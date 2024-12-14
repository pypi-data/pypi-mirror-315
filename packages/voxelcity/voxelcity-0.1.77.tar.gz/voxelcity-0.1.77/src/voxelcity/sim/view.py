import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from numba import njit, prange

from ..file.geojson import find_building_containing_point
from ..file.obj import grid_to_obj, export_obj

# JIT-compiled trace_ray function
@njit
def trace_ray(voxel_data, origin, direction):
    nx, ny, nz = voxel_data.shape
    x0, y0, z0 = origin
    dx, dy, dz = direction

    # Normalize direction
    length = np.sqrt(dx*dx + dy*dy + dz*dz)
    if length == 0.0:
        return False
    dx /= length
    dy /= length
    dz /= length

    # Initialize variables
    x, y, z = x0 + 0.5, y0 + 0.5, z0 + 0.5  # Start at center of voxel
    i, j, k = int(x0), int(y0), int(z0)

    # Determine the step direction
    step_x = 1 if dx >= 0 else -1
    step_y = 1 if dy >= 0 else -1
    step_z = 1 if dz >= 0 else -1

    # Compute tMax and tDelta
    if dx != 0:
        t_max_x = ((i + (step_x > 0)) - x) / dx
        t_delta_x = abs(1 / dx)
    else:
        t_max_x = np.inf
        t_delta_x = np.inf

    if dy != 0:
        t_max_y = ((j + (step_y > 0)) - y) / dy
        t_delta_y = abs(1 / dy)
    else:
        t_max_y = np.inf
        t_delta_y = np.inf

    if dz != 0:
        t_max_z = ((k + (step_z > 0)) - z) / dz
        t_delta_z = abs(1 / dz)
    else:
        t_max_z = np.inf
        t_delta_z = np.inf

    while (0 <= i < nx) and (0 <= j < ny) and (0 <= k < nz):
        # Check voxel value
        voxel_value = voxel_data[i, j, k]
        if voxel_value in (-2, 2, 5, 7):  # Green voxel types
            return True

        # Move to next voxel boundary
        if t_max_x < t_max_y:
            if t_max_x < t_max_z:
                t_max = t_max_x
                t_max_x += t_delta_x
                i += step_x
            else:
                t_max = t_max_z
                t_max_z += t_delta_z
                k += step_z
        else:
            if t_max_y < t_max_z:
                t_max = t_max_y
                t_max_y += t_delta_y
                j += step_y
            else:
                t_max = t_max_z
                t_max_z += t_delta_z
                k += step_z

    return False  # Did not hit a green voxel

# JIT-compiled compute_gvi function
@njit
def compute_gvi(observer_location, voxel_data, ray_directions):
    green_count = 0
    total_rays = ray_directions.shape[0]

    for idx in range(total_rays):
        direction = ray_directions[idx]
        if trace_ray(voxel_data, observer_location, direction):
            green_count += 1

    green_view_index = green_count / total_rays
    return green_view_index

# JIT-compiled function to compute GVI map
@njit(parallel=True)
def compute_gvi_map(voxel_data, ray_directions, view_height_voxel=0):
    nx, ny, nz = voxel_data.shape
    gvi_map = np.full((nx, ny), np.nan)

    for x in prange(nx):
        for y in range(ny):
            found_observer = False
            for z in range(1, nz):
                if voxel_data[x, y, z] in (0, -2) and voxel_data[x, y, z - 1] not in (0, -2):
                    if voxel_data[x, y, z - 1] in (-3, 7, 8, 9):
                        gvi_map[x, y] = np.nan
                        found_observer = True
                        break
                    else:
                        observer_location = np.array([x, y, z+view_height_voxel], dtype=np.float64)
                        gvi_value = compute_gvi(observer_location, voxel_data, ray_directions)
                        gvi_map[x, y] = gvi_value
                        found_observer = True
                        break
            if not found_observer:
                gvi_map[x, y] = np.nan

    return np.flipud(gvi_map)

# Main script
# Load or define your voxel data (3D numpy array)
# For demonstration, let's create a small voxel_data array
# In practice, you would load your actual data
# voxel_data = np.random.randint(-3, 8, size=(100, 100, 50))
# Replace the above line with your actual voxel data
# voxel_data = voxelcity_grid  # Ensure voxelcity_grid is defined in your environment




def get_green_view_index(voxel_data, meshsize, **kwargs):

    view_point_height = kwargs.get("view_point_height", 1.5)
    view_height_voxel = int(view_point_height / meshsize)

    colormap = kwargs.get("colormap", 'viridis')

    # Define parameters for ray emission
    N_azimuth = 60  # Number of horizontal angles
    N_elevation = 10  # Number of vertical angles within the specified range
    elevation_min_degrees = -30    # Minimum elevation angle (in degrees)
    elevation_max_degrees = 30   # Maximum elevation angle (in degrees)

    # Generate ray directions
    azimuth_angles = np.linspace(0, 2 * np.pi, N_azimuth, endpoint=False)
    elevation_angles = np.deg2rad(np.linspace(elevation_min_degrees, elevation_max_degrees, N_elevation))

    ray_directions = []
    for elevation in elevation_angles:
        cos_elev = np.cos(elevation)
        sin_elev = np.sin(elevation)
        for azimuth in azimuth_angles:
            dx = cos_elev * np.cos(azimuth)
            dy = cos_elev * np.sin(azimuth)
            dz = sin_elev
            ray_directions.append([dx, dy, dz])

    ray_directions = np.array(ray_directions, dtype=np.float64)

    # Compute the GVI map using the optimized function
    gvi_map = compute_gvi_map(voxel_data, ray_directions, view_height_voxel=view_height_voxel)

    # Create a copy of the inverted 'BuPu' colormap
    cmap = plt.cm.get_cmap(colormap).copy()

    # Set the 'bad' color (for np.nan values) to gray
    # cmap.set_bad(color='#202020')
    cmap.set_bad(color='lightgray')

    # Visualization of the SVI map in 2D with inverted 'BuPu' colormap and gray for np.nan
    plt.figure(figsize=(10, 8))
    plt.imshow(gvi_map, origin='lower', cmap=cmap)
    plt.colorbar(label='Green View Index')
    # plt.title('Green View Index Map with Inverted BuPu Colormap (NaN as Gray)')
    # plt.xlabel('X Coordinate')
    # plt.ylabel('Y Coordinate')
    plt.show()

    # Visualization of the SVI map in 2D with inverted 'BuPu' colormap and gray for np.nan
    # plt.figure(figsize=(10, 8))
    # plt.imshow(np.flipud(gvi_map), origin='lower', cmap=cmap)
    # plt.axis('off')  # Remove axes, ticks, and tick numbers
    # # plt.colorbar(label='Sky View Index')
    # # plt.title('Sky View Index Map with Inverted BuPu Colormap (NaN as Gray)')
    # # plt.xlabel('X Coordinate')
    # # plt.ylabel('Y Coordinate')
    # plt.show()

# view_kwargs = {
#     "view_point_height": 1.5, # To set height of view point in meters. Default: 1.5 m.
#     "obj_export": True,
#     "output_directory": 'output/test', # To set directory path for output files. Default: False.
#     "output_file_name": 'gvi_test', # To set file name excluding extension. Default: 'view_index.
#     "colormap_name": 'viridis', # Choose a colormap
#     "num_colors": 10, # Number of discrete colors
#     "alpha_value": 1.0, # Set transparency (0.0 to 1.0)
#     "vmin_value": 0.0, # Minimum value for colormap normalization
#     "vmax_value": 1.0 # Maximum value for colormap normalization
# }

    obj_export = kwargs.get("obj_export")
    if obj_export == True:
        dem_grid = kwargs.get("dem_grid", np.zeros_like(gvi_map))
        output_dir = kwargs.get("output_directory", "output")
        output_file_name = kwargs.get("output_file_name", "view_index")        
        num_colors = kwargs.get("num_colors", 10)
        alpha = kwargs.get("alpha", 1.0)
        vmin = kwargs.get("vmin", 0.0)
        vmax = kwargs.get("vmax", 1.0)
        grid_to_obj(
            gvi_map,
            dem_grid,
            output_dir,
            output_file_name,
            meshsize,
            view_point_height,
            colormap_name=colormap,
            num_colors=num_colors,
            alpha=alpha,
            vmin=vmin,
            vmax=vmax
        )

    return gvi_map

# JIT-compiled trace_ray_sky function
@njit
def trace_ray_sky(voxel_data, origin, direction):
    nx, ny, nz = voxel_data.shape
    x0, y0, z0 = origin
    dx, dy, dz = direction

    # Normalize direction
    length = np.sqrt(dx*dx + dy*dy + dz*dz)
    if length == 0.0:
        return False
    dx /= length
    dy /= length
    dz /= length

    # Initialize variables
    x, y, z = x0 + 0.5, y0 + 0.5, z0 + 0.5  # Start at center of voxel
    i, j, k = int(x0), int(y0), int(z0)

    # Determine the step direction
    step_x = 1 if dx >= 0 else -1
    step_y = 1 if dy >= 0 else -1
    step_z = 1 if dz >= 0 else -1

    # Compute tMax and tDelta
    if dx != 0:
        t_max_x = ((i + (step_x > 0)) - x) / dx
        t_delta_x = abs(1 / dx)
    else:
        t_max_x = np.inf
        t_delta_x = np.inf

    if dy != 0:
        t_max_y = ((j + (step_y > 0)) - y) / dy
        t_delta_y = abs(1 / dy)
    else:
        t_max_y = np.inf
        t_delta_y = np.inf

    if dz != 0:
        t_max_z = ((k + (step_z > 0)) - z) / dz
        t_delta_z = abs(1 / dz)
    else:
        t_max_z = np.inf
        t_delta_z = np.inf

    while (0 <= i < nx) and (0 <= j < ny) and (0 <= k < nz):
        # Check voxel value
        voxel_value = voxel_data[i, j, k]
        if voxel_value != 0:  # Non-void voxel types (obstacles)
            return False  # Ray is blocked by an obstacle

        # Move to next voxel boundary
        if t_max_x < t_max_y:
            if t_max_x < t_max_z:
                t_max = t_max_x
                t_max_x += t_delta_x
                i += step_x
            else:
                t_max = t_max_z
                t_max_z += t_delta_z
                k += step_z
        else:
            if t_max_y < t_max_z:
                t_max = t_max_y
                t_max_y += t_delta_y
                j += step_y
            else:
                t_max = t_max_z
                t_max_z += t_delta_z
                k += step_z

    # Ray has reached outside the voxel grid without hitting any obstacles
    return True

# JIT-compiled compute_svi function
@njit
def compute_svi(observer_location, voxel_data, ray_directions):
    sky_count = 0
    total_rays = ray_directions.shape[0]

    for idx in range(total_rays):
        direction = ray_directions[idx]
        if trace_ray_sky(voxel_data, observer_location, direction):
            sky_count += 1

    sky_view_index = sky_count / total_rays
    return sky_view_index

# JIT-compiled function to compute SVI map
@njit(parallel=True)
def compute_svi_map(voxel_data, ray_directions, view_height_voxel=0):
    nx, ny, nz = voxel_data.shape
    svi_map = np.full((nx, ny), np.nan)

    for x in prange(nx):
        for y in range(ny):
            found_observer = False
            for z in range(1, nz):
                if voxel_data[x, y, z] in (0, -2) and voxel_data[x, y, z - 1] not in (0, -2):
                    if voxel_data[x, y, z - 1] in (-3, 7, 8, 9):
                        svi_map[x, y] = np.nan
                        found_observer = True
                        break
                    else:
                        observer_location = np.array([x, y, z+view_height_voxel], dtype=np.float64)
                        svi_value = compute_svi(observer_location, voxel_data, ray_directions)
                        svi_map[x, y] = svi_value
                        found_observer = True
                        break
            if not found_observer:
                svi_map[x, y] = np.nan

    return np.flipud(svi_map)

# Main script modifications
# Load or define your voxel data (3D numpy array)
# voxel_data = voxelcity_grid  # Ensure voxelcity_grid is defined in your environment

def get_sky_view_index(voxel_data, meshsize, **kwargs):

    view_point_height = kwargs.get("view_point_height", 1.5)
    view_height_voxel = int(view_point_height / meshsize)

    colormap = kwargs.get("colormap", 'viridis')

    # Define parameters for ray emission for SVI
    # For SVI, we focus on upward directions
    N_azimuth_svi = 60  # Number of horizontal angles
    N_elevation_svi = 5  # Number of vertical angles within the specified range
    elevation_min_degrees_svi = 0   # Minimum elevation angle (in degrees)
    elevation_max_degrees_svi = 30   # Maximum elevation angle (in degrees)

    # Generate ray directions for SVI
    azimuth_angles_svi = np.linspace(0, 2 * np.pi, N_azimuth_svi, endpoint=False)
    elevation_angles_svi = np.deg2rad(np.linspace(elevation_min_degrees_svi, elevation_max_degrees_svi, N_elevation_svi))

    ray_directions_svi = []
    for elevation in elevation_angles_svi:
        cos_elev = np.cos(elevation)
        sin_elev = np.sin(elevation)
        for azimuth in azimuth_angles_svi:
            dx = cos_elev * np.cos(azimuth)
            dy = cos_elev * np.sin(azimuth)
            dz = sin_elev
            ray_directions_svi.append([dx, dy, dz])

    ray_directions_svi = np.array(ray_directions_svi, dtype=np.float64)

    # Compute the SVI map using the optimized function
    svi_map = compute_svi_map(voxel_data, ray_directions_svi, view_height_voxel=view_height_voxel)

    # Create a copy of the inverted 'BuPu' colormap
    cmap = plt.cm.get_cmap(colormap).copy()

    # Set the 'bad' color (for np.nan values) to gray
    # cmap.set_bad(color='#202020')
    cmap.set_bad(color='lightgray')

    # Visualization of the SVI map in 2D with inverted 'BuPu' colormap and gray for np.nan
    plt.figure(figsize=(10, 8))
    plt.imshow(svi_map, origin='lower', cmap=cmap)
    plt.colorbar(label='Sky View Index')
    # plt.title('Sky View Index Map with Inverted BuPu Colormap (NaN as Gray)')
    # plt.xlabel('X Coordinate')
    # plt.ylabel('Y Coordinate')
    plt.show()

    # Visualization of the SVI map in 2D with inverted 'BuPu' colormap and gray for np.nan
    # plt.figure(figsize=(10, 8))
    # plt.imshow(np.flipud(svi_map), origin='lower', cmap=cmap)
    # plt.axis('off')  # Remove axes, ticks, and tick numbers
    # # plt.colorbar(label='Sky View Index')
    # # plt.title('Sky View Index Map with Inverted BuPu Colormap (NaN as Gray)')
    # # plt.xlabel('X Coordinate')
    # # plt.ylabel('Y Coordinate')
    # plt.show()

    obj_export = kwargs.get("obj_export")
    if obj_export == True:
        dem_grid = kwargs.get("dem_grid", np.zeros_like(svi_map))
        output_dir = kwargs.get("output_directory", "output")
        output_file_name = kwargs.get("output_file_name", "view_index")        
        num_colors = kwargs.get("num_colors", 10)
        alpha = kwargs.get("alpha", 1.0)
        vmin = kwargs.get("vmin", 0.0)
        vmax = kwargs.get("vmax", 1.0)
        grid_to_obj(
            svi_map,
            dem_grid,
            output_dir,
            output_file_name,
            meshsize,
            view_point_height,
            colormap_name=colormap,
            num_colors=num_colors,
            alpha=alpha,
            vmin=vmin,
            vmax=vmax
        )

    return svi_map

def mark_building_by_id(voxelcity_grid, building_id_grid_ori, ids, mark):

    building_id_grid = np.flipud(building_id_grid_ori.copy())

    # Get x,y positions from building_id_grid where landmarks are
    positions = np.where(np.isin(building_id_grid, ids))

    # Loop through each x,y position
    for i in range(len(positions[0])):
        x, y = positions[0][i], positions[1][i]
        # Replace -3s with -10s at this x,y position for all z
        z_mask = voxelcity_grid[x, y, :] == -3
        voxelcity_grid[x, y, z_mask] = mark

@njit
def trace_ray_to_target(voxel_data, origin, target, opaque_values):
    nx, ny, nz = voxel_data.shape
    x0, y0, z0 = origin
    x1, y1, z1 = target
    dx = x1 - x0
    dy = y1 - y0
    dz = z1 - z0

    # Normalize direction
    length = np.sqrt(dx*dx + dy*dy + dz*dz)
    if length == 0.0:
        return True  # Origin and target are at the same location
    dx /= length
    dy /= length
    dz /= length

    # Initialize variables
    x, y, z = x0 + 0.5, y0 + 0.5, z0 + 0.5  # Start at center of voxel
    i, j, k = int(x0), int(y0), int(z0)

    # Determine the step direction
    step_x = 1 if dx >= 0 else -1
    step_y = 1 if dy >= 0 else -1
    step_z = 1 if dz >= 0 else -1

    # Compute tMax and tDelta
    if dx != 0:
        t_max_x = ((i + (step_x > 0)) - x) / dx
        t_delta_x = abs(1 / dx)
    else:
        t_max_x = np.inf
        t_delta_x = np.inf

    if dy != 0:
        t_max_y = ((j + (step_y > 0)) - y) / dy
        t_delta_y = abs(1 / dy)
    else:
        t_max_y = np.inf
        t_delta_y = np.inf

    if dz != 0:
        t_max_z = ((k + (step_z > 0)) - z) / dz
        t_delta_z = abs(1 / dz)
    else:
        t_max_z = np.inf
        t_delta_z = np.inf

    # Main loop
    while True:
        # Check voxel value
        if (0 <= i < nx) and (0 <= j < ny) and (0 <= k < nz):
            voxel_value = voxel_data[i, j, k]
            if voxel_value in opaque_values:
                return False  # Ray is blocked
        else:
            return False  # Out of bounds

        # Check if we have reached the target voxel
        if i == int(x1) and j == int(y1) and k == int(z1):
            return True  # Ray has reached the target

        # Move to next voxel boundary
        if t_max_x < t_max_y:
            if t_max_x < t_max_z:
                t_max = t_max_x
                t_max_x += t_delta_x
                i += step_x
            else:
                t_max = t_max_z
                t_max_z += t_delta_z
                k += step_z
        else:
            if t_max_y < t_max_z:
                t_max = t_max_y
                t_max_y += t_delta_y
                j += step_y
            else:
                t_max = t_max_z
                t_max_z += t_delta_z
                k += step_z

@njit
def compute_visibility_to_all_landmarks(observer_location, landmark_positions, voxel_data, opaque_values):
    # Check visibility to all landmarks
    for idx in range(landmark_positions.shape[0]):
        target = landmark_positions[idx].astype(np.float64)
        is_visible = trace_ray_to_target(voxel_data, observer_location, target, opaque_values)
        if is_visible:
            return 1  # Visible to at least one landmark
    return 0  # Not visible to any landmarks

@njit(parallel=True)
def compute_visibility_map(voxel_data, landmark_positions, opaque_values, view_height_voxel):
    nx, ny, nz = voxel_data.shape
    visibility_map = np.full((nx, ny), np.nan)

    for x in prange(nx):
        for y in range(ny):
            found_observer = False
            for z in range(1, nz):
                if voxel_data[x, y, z] == 0 and voxel_data[x, y, z - 1] != 0:
                    # This is the lowest void cell
                    if voxel_data[x, y, z - 1] in (-3, -2, 7, 8, 9):  # Building or tree below
                        visibility_map[x, y] = np.nan
                        found_observer = True
                        break
                    else:
                        observer_location = np.array([x, y, z+view_height_voxel], dtype=np.float64)
                        visible = compute_visibility_to_all_landmarks(observer_location, landmark_positions, voxel_data, opaque_values)
                        visibility_map[x, y] = visible
                        found_observer = True
                        break
            if not found_observer:
                visibility_map[x, y] = np.nan

    return visibility_map

def compute_landmark_visibility(voxel_data, target_value=-30, view_height_voxel=0, colormap='viridis'):
    # Find landmark positions
    landmark_positions = np.argwhere(voxel_data == target_value)

    if landmark_positions.shape[0] == 0:
        raise ValueError(f"No landmark with value {target_value} found in the voxel data.")

    # Define opaque voxel values (values that block the ray)
    # Opaque values are all values except 0 (void) and the target_value (landmark)
    unique_values = np.unique(voxel_data)
    opaque_values = np.array([v for v in unique_values if v != 0 and v != target_value], dtype=np.int32)

    # Compute the visibility map
    visibility_map = compute_visibility_map(voxel_data, landmark_positions, opaque_values, view_height_voxel)

    # Visualization of the visibility map in 2D
    cmap = plt.cm.get_cmap(colormap, 2).copy()
    cmap.set_bad(color='lightgray')

    plt.figure(figsize=(10, 8))
    plt.imshow(np.flipud(visibility_map), origin='lower', cmap=cmap, vmin=0, vmax=1)
    # plt.colorbar(label='Visibility (1: Visible, 0: Not Visible)')

    # Create legend handles
    visible_patch = mpatches.Patch(color=cmap(1.0), label='Visible (1)')
    not_visible_patch = mpatches.Patch(color=cmap(0.0), label='Not Visible (0)')

    # Add legend
    plt.legend(handles=[visible_patch, not_visible_patch], 
            loc='center left',  # You can adjust location as needed
            bbox_to_anchor=(1.0, 0.5))  # This places legend to the right of the plot
    
    # plt.title('Landmark Visibility Map')
    # plt.xlabel('X Coordinate')
    # plt.ylabel('Y Coordinate')
    plt.show()

    # Alternative visualization
    # plt.figure(figsize=(10, 8))
    # plt.imshow(np.flipud(visibility_map), origin='lower', cmap=cmap, vmin=0, vmax=1)
    # plt.axis('off')  # Remove axes, ticks, and tick numbers
    # plt.show()

    return np.flipud(visibility_map)

def get_landmark_visibility_map(voxelcity_grid, building_id_grid, building_geojson, meshsize, **kwargs):

    view_point_height = kwargs.get("view_point_height", 1.5)
    view_height_voxel = int(view_point_height / meshsize)

    colormap = kwargs.get("colormap", 'viridis')

    # Paste your GeoJSON features directly into the features variable
    features = building_geojson  # Continue with your full data...

    landmark_ids = kwargs.get('landmark_building_ids', None)
    if landmark_ids is None:
        rectangle_vertices = kwargs.get("rectangle_vertices", None)
        if rectangle_vertices is None:
            print("Cannot set landmark buildings. You need to input either of rectangle_vertices or landmark_ids.")
            return None
        # Extract all latitudes and longitudes
        lats = [coord[0] for coord in rectangle_vertices]
        lons = [coord[1] for coord in rectangle_vertices]
        
        # Calculate center by averaging min and max values
        center_lat = (min(lats) + max(lats)) / 2
        center_lon = (min(lons) + max(lons)) / 2
        
        target_point = (center_lat, center_lon)
        landmark_ids = find_building_containing_point(features, target_point)

    target_value = -30
    mark_building_by_id(voxelcity_grid, building_id_grid, landmark_ids, target_value)
    landmark_vis_map = compute_landmark_visibility(voxelcity_grid, target_value=target_value, view_height_voxel=view_height_voxel, colormap=colormap)

    obj_export = kwargs.get("obj_export")
    if obj_export == True:
        dem_grid = kwargs.get("dem_grid", np.zeros_like(landmark_vis_map))
        output_dir = kwargs.get("output_directory", "output")
        output_file_name = kwargs.get("output_file_name", "landmark_visibility")        
        num_colors = 2
        alpha = kwargs.get("alpha", 1.0)
        vmin = kwargs.get("vmin", 0.0)
        vmax = kwargs.get("vmax", 1.0)
        grid_to_obj(
            landmark_vis_map,
            dem_grid,
            output_dir,
            output_file_name,
            meshsize,
            view_point_height,
            colormap_name=colormap,
            num_colors=num_colors,
            alpha=alpha,
            vmin=vmin,
            vmax=vmax
        )
        output_file_name_vox = 'voxcity_' + output_file_name
        export_obj(voxelcity_grid, output_dir, output_file_name_vox, meshsize)

    return landmark_vis_map