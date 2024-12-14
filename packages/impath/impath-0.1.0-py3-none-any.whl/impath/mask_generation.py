import cv2
import json
import numpy as np
import sys
import os
import gc
import hashlib
import requests
from PIL import Image, ImageFile


# Allow truncated image loading
Image.MAX_IMAGE_PIXELS = None
ImageFile.LOAD_TRUNCATED_IMAGES = True

'''
Initial handling of images
'''

def get_md5_hash(file_path):
    '''
    Calculate the MD5 hash of a file.

    This function reads the file in chunks to handle large files efficiently 
    and computes the MD5 hash of the file's contents.

    Args:
        file_path (str): The path to the file for which the MD5 hash is calculated.

    Returns:
        str: The hexadecimal representation of the MD5 hash.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        PermissionError: If the file cannot be accessed due to insufficient permissions.
    '''
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        # Read the file in chunks to avoid memory issues with large files
        while chunk := f.read(8192):
            md5.update(chunk)
    return md5.hexdigest()

def get_item_tiles(item_id, dsa_url, girder_token):
    '''
    Fetch metadata for image tiles associated with an item from the Girder API.

    This function queries the Girder-based Digital Slide Archive (DSA) API to 
    retrieve tile metadata for a specified item. The request is authenticated 
    using a Girder token.

    Args:
        item_id (str): The ID of the item whose tile metadata is to be retrieved.
        dsa_url (str): The base URL of the Digital Slide Archive instance.
        girder_token (str): The authentication token for the Girder API.

    Returns:
        dict: A dictionary containing the tile metadata returned by the API.

    Raises:
        requests.exceptions.RequestException: If the API request fails.
        ValueError: If the response is not valid JSON.
    '''
    resp = requests.get(
        url = f'{dsa_url}/api/v1/item/{item_id}/tiles',
        headers = {
            'Girder-Token': girder_token
        }
    )
    return resp.json()

def get_item_info(item_id, dsa_url, girder_token):
    '''
    Retrieve detailed information about a specific item from the Girder API.

    This function sends a GET request to the Digital Slide Archive (DSA) Girder-based 
    API to fetch metadata and details of a specified item. The request is authenticated 
    using a Girder token.

    Args:
        item_id (str): The ID of the item to retrieve information for.
        dsa_url (str): The base URL of the Digital Slide Archive instance.
        girder_token (str): The authentication token for the Girder API.

    Returns:
        dict: A dictionary containing metadata and information about the specified item.

    Raises:
        requests.exceptions.RequestException: If the API request fails.
        ValueError: If the response is not valid JSON.
    '''
    resp = requests.get(
        url = f'{dsa_url}/api/v1/item/{item_id}',
        headers = {
            'Girder-Token': girder_token
        }
    )
    return resp.json()

def get_item_annotations(item_id, dsa_url, girder_token, save_files=False):
    '''
    Retrieve annotations for a specific item from the Girder API.

    This function sends a GET request to the Digital Slide Archive (DSA) API to 
    fetch all annotations associated with a specified item. Optionally, it can 
    save the annotations to a JSON file.

    Args:
        item_id (str): The ID of the item to retrieve annotations for.
        dsa_url (str): The base URL of the Digital Slide Archive instance.
        girder_token (str): The authentication token for the Girder API.
        save_files (bool, optional): If True, saves the annotations to a JSON file 
            in the `./annotations/annotations/` directory. Default is False.

    Returns:
        list: A list of dictionaries containing annotations for the specified item.

    Raises:
        requests.exceptions.RequestException: If the API request fails.
        ValueError: If the response is not valid JSON.
        OSError: If there is an error saving the annotations file.
    '''
    resp = requests.get(
        url = f'{dsa_url}/api/v1/annotation/item/{item_id}',
        headers = {
            'Girder-Token': girder_token
        }
    )
    if save_files:
        with open(f'./annotations/annotations/{item_id}.json', 'w+') as file:
            json.dump(resp.json(), file, indent=4)
    return resp.json()

def resize_and_pad_image(
        file_path, 
        target_width, 
        target_height, 
        background_color=(255,255,255)
    ):
    '''
    Resize an image to fit within target dimensions while maintaining its aspect ratio, 
    and pad the remaining space with a specified background color.

    This function opens an image from the specified file path, resizes it to fit within 
    the target width and height while preserving its aspect ratio, and then centers 
    the resized image on a canvas of the specified target dimensions. The remaining 
    space is filled with the given background color. The resulting image overwrites 
    the original file.

    Args:
        file_path (str): The file path to the image to be resized and padded.
        target_width (int): The width of the target image.
        target_height (int): The height of the target image.
        background_color (tuple, optional): The RGB color to use for padding. 
            Default is white (255, 255, 255).

    Returns:
        None

    Notes:
        - The function overwrites the original image file at `file_path`.
        - The image is saved in "RGBA" mode, which supports transparency.

    Raises:
        FileNotFoundError: If the image file does not exist.
        OSError: If there is an issue opening or saving the image.
        ValueError: If `target_width` or `target_height` is non-positive.
    '''
    image = Image.open(file_path)
    # Calculate the aspect ratio
    aspect_ratio = min(target_width / image.width, target_height / image.height)
    # Calculate the new dimensions
    new_size = (int(image.width * aspect_ratio), int(image.height * aspect_ratio))
    # Resize the image with the aspect ratio preserved
    image = image.resize(new_size, Image.LANCZOS)
    # Create a new image with the target dimensions and the specified background color
    new_image = Image.new("RGBA", (target_width, target_height), background_color)
    # Paste the resized image onto the center of the new image
    new_image.paste(image, (0, 0))
    
    new_image.save(file_path)

def download_scaled_image(
        item_id, 
        dsa_url, 
        girder_token, 
        masks_directory='', 
        dataset_id='', 
        scale=None, 
        overwrite_old=True, 
        original_size=None
    ):
    '''
    Download and optionally scale an image from the Digital Slide Archive (DSA) API.

    This function fetches an image file associated with a specified item ID from the DSA, 
    saves it to a structured directory, and optionally resizes it to a specified scale. 
    The function can also overwrite existing files or skip downloads if a matching image 
    already exists.

    Args:
        item_id (str): The ID of the item to download the image for.
        dsa_url (str): The base URL of the Digital Slide Archive instance.
        girder_token (str): The authentication token for the Girder API.
        masks_directory (str, optional): The base directory to save the downloaded image. 
            Default is an empty string.
        dataset_id (str, optional): The dataset ID used to organize images into folders. 
            Default is an empty string.
        scale (tuple, optional): Target width and height (in pixels) to resize the image. 
            If None, downloads the original size. Default is None.
        overwrite_old (bool, optional): If True, overwrites existing images. If False, skips 
            downloading if a matching file already exists. Default is True.
        original_size (tuple, optional): Expected original dimensions of the image 
            (width, height). Used to verify existing files. Default is None.

    Returns:
        tuple: A tuple containing:
            - folder_id (str): The folder ID where the item resides.
            - file_id (str): The file ID of the downloaded image.
            - file_name (str): The name of the downloaded image file.
            - file_path (str): The full file path to the downloaded image.

    Raises:
        requests.exceptions.RequestException: If the API request fails.
        OSError: If there is an issue creating directories or writing files.
        Exception: If the downloaded file size does not match the expected size.

    Notes:
        - The function uses the `resize_and_pad_image` utility to resize and pad images when 
          the `scale` parameter is provided.
        - The image is saved in a structured directory based on `masks_directory` and 
          `dataset_id`.
    '''
    info = get_item_info(item_id, dsa_url, girder_token)
    folder_id = info['folderId']
    file_id = info['largeImage']['fileId']
    file_name = info['name']

    print(info)

    slides_folder = os.path.join(masks_directory, dataset_id)
    if not os.path.exists(slides_folder):
        os.makedirs(slides_folder)
    masks_folder = os.path.join(masks_directory, dataset_id, item_id)
    if not os.path.exists(masks_folder):
        os.makedirs(masks_folder)

    if scale:
        file_name =  os.path.splitext(os.path.basename(file_name))[0] + '.png'
    elif os.path.isfile(os.path.splitext(os.path.basename(file_name))[0] + '.png'):
        os.remove(os.path.splitext(os.path.basename(file_name))[0] + '.png')
    
    file_path = os.path.join(masks_folder, file_name)

    if overwrite_old and os.path.isfile(file_path):
        with Image.open(file_path) as img:
            current_height, current_width = img.size
        if scale and current_width == scale[0] and current_height == scale[1]:
            print(f'{file_path} already exists')
            return folder_id, file_id, file_name, file_path
        elif original_size and current_width == original_size[0] and current_height == original_size[1]:
            print(f'{file_path} already exists')
            return folder_id, file_id, file_name, file_path    

    if scale:
        file_download_url = f'{dsa_url}/api/v1/item/{item_id}/tiles/region'
        params = {
            'units': 'base_pixels',
            'width': scale[0],
            'height': scale[1],
            'encoding': 'PNG',
            'exact': 'false',
            'jpegQuality': 95,
            'jpegSubsampling': 0
        }
    else:
        file_download_url = f'{dsa_url}/api/v1/file/{file_id}/download'
        params = {
            
        }

    response = requests.get(
        file_download_url, 
        headers = {
            # 'accept': 'image/png',
            'Girder-Token': girder_token
        },
        params = params,
        stream=True
    )
    response.raise_for_status()
    # print(response.headers)

    total_size = info['size'] #int(response.headers.get('content-length', 0))
    # print(total_size)
    downloaded_size = 0
    print(file_path)
    with open(file_path, 'wb+') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
                downloaded_size += len(chunk)
    print(f'Downloaded: {downloaded_size}')
    print(os.path.exists(file_path))
    if downloaded_size != total_size:
        os.remove(file_path)
        raise Exception(f"Incomplete download: {downloaded_size} bytes downloaded, expected {total_size} bytes")
    if scale:
        resize_and_pad_image(file_path, scale[0], scale[1]) # COMMENT THIS OUT IF FIT TO SIZE NOT NECESSARY
    return folder_id, file_id, file_name, file_path



'''
Mask generation
'''


def create_mask(image_shape, shapes):
    '''
    Generate a mask from a list of shapes and their coordinates.

    This function creates a binary or colored mask of the specified dimensions by drawing shapes 
    onto it based on the given coordinates. Shapes are sorted by area to ensure efficient 
    processing, and overlapping regions are handled to avoid redundant drawing.

    Args:
        image_shape (tuple): Dimensions of the output mask in the format `(height, width, channels)`. 
            If channels are not provided, it assumes a grayscale mask.
        shapes (list): A list of dictionaries representing shapes to be drawn. Each dictionary 
            should have the following keys:
            - 'coordinates' (list of tuples): Coordinates of the shape's vertices. Each vertex 
              should be a tuple `(x, y)`.
            - 'color' (int or tuple): Color value to fill the shape with. For grayscale masks, 
              provide an integer; for RGB masks, provide a tuple `(R, G, B)`.

    Returns:
        numpy.ndarray: The generated mask as a NumPy array.

    Notes:
        - The function sorts shapes by their area, ensuring that larger shapes are processed first.
        - Overlapping regions are handled by checking if a point in the shape overlaps a previously 
          drawn shape.
        - The mask is initialized with zeros, which represent the background.

    Example:
        ```python
        image_shape = (512, 512, 3)
        shapes = [
            {'coordinates': [(10, 10), (100, 10), (100, 100), (10, 100)], 'color': (255, 0, 0)},
            {'coordinates': [(50, 50), (150, 50), (150, 150), (50, 150)], 'color': (0, 255, 0)},
        ]
        mask = create_mask(image_shape, shapes)
        ```
    '''
    # Create a blank mask
    mask = np.zeros(image_shape[:2], dtype=np.uint8)

    # Sort shapes by area for efficient processing
    sorted_shapes = sorted(shapes, key=lambda shape: calculate_contour_area(shape['coordinates']), reverse=True)

    # Track processed contours to handle overlapping regions
    filled_contours = []

    for shape in sorted_shapes:
        # Convert coordinates to a numpy array suitable for OpenCV
        points = np.array(shape['coordinates'], dtype=np.int32).reshape((-1, 1, 2))

        # Process overlaps only if the mask isn't empty and contours are stored
        if filled_contours:
            overlap_found = False
            for i, contour in enumerate(filled_contours):
                # Check if this shape overlaps a previously filled contour
                temp_point = (int(points[0][0][0]), int(points[0][0][1]))
                if cv2.pointPolygonTest(contour, temp_point, False) > 0:
                    cv2.fillPoly(mask, [points], shape['color'])
                    del filled_contours[i]
                    overlap_found = True
                    break
            # Skip to next if overlap was handled
            if overlap_found:
                continue

        # Draw the shape if no overlaps were found
        cv2.fillPoly(mask, [points], shape['color'])
        filled_contours.append(points)

    return mask


def calculate_contour_area(coordinates):
    # Convert points to numpy array
    points = np.array(coordinates, np.int32)
    # Reshape the array into a 2D array with 1 row
    points = points.reshape((-1, 1, 2))
    # Calculate the contour area
    area = cv2.contourArea(points)
    return area



def get_resized_mask(mask, color, binary_memmap_file, height, width, output_size):
    # Define dtype (uint8 for binary masks)
    dtype = np.uint8
    if output_size:
        resized_mask = np.memmap(binary_memmap_file, dtype=dtype, mode='w+', shape=(output_size[1], output_size[0]))
        resized_portion = cv2.resize((mask == color).astype(dtype) * 255, output_size, interpolation=cv2.INTER_NEAREST)
        resized_mask[:, :] = resized_portion
        resized_mask.flush()
    else:
        resized_mask = np.memmap(binary_memmap_file, dtype=dtype, mode='w+', shape=(height, width))

        # Break down the mask assignment in chunks to avoid high memory usage
        chunk_size = 20000  # Process 20000 rows at a time (adjust this if necessary)
        for start_row in range(0, height, chunk_size):
            end_row = min(start_row + chunk_size, height)
            resized_mask[start_row:end_row, :] = (mask[start_row:end_row, :] == color).astype(dtype) * 255
            resized_mask.flush()  # Ensure each chunk is written to disk after processing

    return resized_mask

def create_individual_images(mask, annotation_colors, outputs_path, output_size=None, overwrite_old=False, output_format='png'):
    print("Creating individual images")
    
    # Determine the final size based on the input mask or resize requirement
    height, width = output_size if output_size else mask.shape[:2]
    print(f'{width}x{height}')

    # Temporary memory-mapped binary mask file path
    binary_memmap_file = f'{outputs_path}/temp_binary_mask.dat'
    # Create a memory-mapped binary mask for the current label only

    # Loop over each label to create individual binary masks one by one
    for label, color in annotation_colors.items():
        # Prepare output file path
        image_name = f'{outputs_path}/mask_{label.replace(" ", "_")}.{output_format}'

        
        
        # Skip if file already exists to save processing time
        if overwrite_old and os.path.isfile(image_name):
            with Image.open(image_name) as img:
                current_width, current_height = img.size
            if current_width == width and current_height == height:
                continue
        binary_mask = get_resized_mask(mask, color, binary_memmap_file, height, width, output_size)
        
        # Save the binary mask to file
        cv2.imwrite(image_name, binary_mask)

        # Cleanup for the current binary mask
        del binary_mask
        gc.collect()  # Force garbage collection to free memory-mapped file
        print(f'{label} finished')

    # Handle the background mask if needed
    background_image_name = f'{outputs_path}/mask_Background.{output_format}'
    if overwrite_old and not os.path.isfile(background_image_name):
        with Image.open(background_image_name) as img:
            current_width, current_height = img.size
        if current_width != width and current_height != height:
            # Reuse the memory-mapped binary mask for the background
            binary_mask = np.memmap(binary_memmap_file, dtype=np.uint8, mode='w+', shape=(height, width))
            binary_mask[:] = (mask == 0).astype(np.uint8) * 255
            cv2.imwrite(background_image_name, binary_mask)
        
        # Cleanup after saving background mask
        del binary_mask
        gc.collect()

    # Remove the temporary binary mask file to free disk space
    if os.path.exists(binary_memmap_file):
        os.remove(binary_memmap_file)

    print("All individual images created successfully.")



def gw_masking(items, masks_directory='', dataset_id='', target_size=None, overwrite_old=True, output_format='tiff'):
    print('Start Masking')
    # start_time = time.time()
    annotation_types = ['Background', 'Gray Matter', 'White Matter', 'Leptomeninges', 'Superficial', 'Other', 'Exclude']
    annotation_colors = {}
    for index, annotation_type in enumerate(annotation_types):
        annotation_colors[annotation_type] = int(255*((index)/(len(annotation_types)+1)))
    # print('Annotation colors:', round(time.time()-start_time, 3))
    
    for item in items:
        item_id = item.get('item_id', None)
        if not item_id:
            print(f'Could not get item_id from {item}')
            continue
        dsa_url = item.get('dsa_url', None)
        if not dsa_url:
            print(f'Could not get dsa_url from {item}')
            continue
        girder_token = item.get('girder_token', None)
        if not girder_token:
            print(f'Could not get girder_token from {item}')
            continue
        item_annotations = get_item_annotations(item_id, dsa_url, girder_token, save_files=False)
        
        # print('Annotations pulled:', round(time.time()-start_time, 3))
        if len(item_annotations) > 0:
            info = get_item_info(item_id, dsa_url, girder_token)
            folder_id = info['folderId']
            file_id = info['largeImage']['fileId']
            file_name = info['name']

            item_tiles = get_item_tiles(item_id, dsa_url, girder_token)
            width, height = item_tiles['sizeY'], item_tiles['sizeX']
            image_shape = (width, height)
            scale_ratio = (1, 1)
            if target_size:
                scale_ratio = (target_size[0]/width, target_size[1]/height)
            
                image_shape = (image_shape[0]*scale_ratio[0], image_shape[1]*scale_ratio[1])
            
            masks_dataset_folder = os.path.join(masks_directory, dataset_id)
            if not os.path.exists(masks_dataset_folder):
                os.makedirs(masks_dataset_folder)

            masks_folder = os.path.join(masks_directory, dataset_id, item_id)
            if not os.path.exists(masks_folder):
                os.makedirs(masks_folder)


            joined_annotations = {}
            for annotations_json in item_annotations:
                if annotations_json['annotation']['description'] == 'Created by the Gray-White Segmentation Web App':
                    if joined_annotations == {}:
                        joined_annotations = annotations_json
                    else:
                        for element in annotations_json['annotation']['elements']:
                            joined_annotations['annotation']['elements'].append(element)
            annotations = []
            scale_factor = min(scale_ratio[0], scale_ratio[1])
            for element in joined_annotations['annotation']['elements']:
                label = element['label']['value']
                color = annotation_colors.get(label, 255)
                annotation = {
                    'label': label,
                    'coordinates': [(point[0]*scale_factor, point[1]*scale_factor) for point in element['points']],
                    'color': color
                }
                annotations.append(annotation)


            download_scaled_image(
                item_id = item_id, 
                dsa_url = dsa_url, 
                girder_token = girder_token, 
                masks_directory = masks_directory, 
                dataset_id = dataset_id, 
                target_size = target_size, 
                overwrite_old = overwrite_old, 
                original_size = (width, height)
            )
            mask = None
            if target_size:
                mask = create_mask(target_size, annotations)
            else:
                mask = create_mask(image_shape, annotations)
            
            if not os.path.isfile(f'{masks_folder}/mask_combined.{output_format}'):
                print('Making Combined Mask')
                cv2.imwrite(f'{masks_folder}/mask_combined.{output_format}', mask)
            print('Making Individual Masks')
            create_individual_images(mask, annotation_colors, masks_folder, target_size, overwrite_old, output_format)
