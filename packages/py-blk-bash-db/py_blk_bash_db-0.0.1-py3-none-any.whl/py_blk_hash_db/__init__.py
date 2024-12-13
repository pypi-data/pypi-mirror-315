import os
import hashlib
import json

from .mylog import logger

# 默认文件快大小
CHUNK_SIZE = 1024 * 1024

# 检查文件是否存在，如果不存在则抛出错误。
def check_file_exists(file_path: str):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"py_blk_bash_db: file not found: {file_path}")

# 创建必要的数据目录
def create_dir(data_directory: str):

    # 检查 'data' 文件夹是否存在，如果不存在则创建它
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    # 在 'data' 文件夹下创建子文件夹
    subdirs = ['json', 'bin']
    for subdir in subdirs:
        subdir_path = os.path.join(data_directory, subdir)
        if not os.path.exists(subdir_path):
            os.makedirs(subdir_path)

# 获取指定文件的大小（以字节为单位）。
def get_file_size(file_path) -> int:
    try:
        size = os.path.getsize(file_path)
        return size
    except FileNotFoundError:
        print(f"file not found: {file_path}")
        return None
    except Exception as e:
        print(f"error when reading file: {e}")
        return None

# 将文件拆分为指定大小的块，并以 SHA-256 哈希值命名。
def split_file(input_file, database: str, chunk_size) -> list:
    filename_arr = []
    filesize = get_file_size(input_file)

    with open(input_file, 'rb') as f:
        chunk_number = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break  # 文件结束

            # 计算 SHA-256 哈希
            sha256_hash = hashlib.sha256(chunk).hexdigest()

            # 创建输出文件名
            output_file = f"{sha256_hash}.bin"
            filename_arr.append(output_file)

            # 写入块到新文件
            binpath = os.path.join(database, "bin", output_file)
            with open(binpath, 'wb') as chunk_file:
                chunk_file.write(chunk)
            
            chunk_number += 1
            ONE_MB = 1048675.0
            rate = min(chunk_number * ONE_MB, filesize) / filesize * 100.0
            logger.info("dumping %6.2f%%, %6d MB from %10.3f MB" % (rate, chunk_number, filesize / ONE_MB))
    return filename_arr

# 计算文件的 SHA-256 哈希值。
def calculate_file_hash(file_path):
    hash_sha256 = hashlib.sha256()

    with open(file_path, 'rb') as f:
        # 逐块读取文件内容以计算哈希值
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)

    return hash_sha256.hexdigest()

# 将列表保存为 JSON 文件，文件名为哈希值。
def save_list_to_json(hash_value, database, data_list):
    json_file_name = f"{hash_value}.json"
    jsonpath = os.path.join(database, "json", json_file_name)
    with open(jsonpath, 'w') as json_file:
        json.dump(data_list, json_file, indent=4)
    logger.info("saving index file to %s" % json_file_name)

# 读入一个文件，并且将其加载到数据库中
def input_file_and_load_into_database(filepath, database):
    check_file_exists(filepath)
    hash_list = split_file(filepath, database, CHUNK_SIZE)
    file_hash = calculate_file_hash(filepath)
    save_list_to_json(file_hash, database, hash_list)

# 将多个文件的内容连接成一个大文件。
def concatenate_files(file_list, output_file):
    error = 0
    with open(output_file, 'wb') as outfile:
        for file_name in file_list:
            try:
                with open(file_name, 'rb') as infile:
                    # 读取文件内容并写入输出文件
                    outfile.write(infile.read())
                logger.info(f"load successfully: {file_name}")
            except FileNotFoundError:
                logger.error(f"file not found: {file_name}")
                error += 1
            except Exception as e:
                logger.error(f"file error when processing {file_name}: {e}")
                error += 1
    logger.info("file loaded and %d error occured." % error)

# 将数据库中的一个指定文件整合出来
def load_file_from_database(outputpath, database_folder, selectjson):
    jsondir = os.path.join(database_folder, "json", selectjson)
    check_file_exists(jsondir)
    filelist = [
        os.path.join(database_folder, "bin", filename)
        for filename in json.load(open(jsondir))
    ]
    concatenate_files(filelist, outputpath)

# 从一个指定文件夹中获取所有 json 文件
def read_json_files(folder_path) -> dict:
    combined_list = []
    
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                try:
                    # 读取 JSON 文件并将列表添加到 combined_list
                    data = json.load(file)
                    if isinstance(data, list):
                        combined_list.extend(data)
                except json.JSONDecodeError:
                    logger.error(f"error decoding json from file: {file_path}")
    
    # 以字典的形式返回
    return {
        json_content: True
        for json_content in combined_list
    }

# 自动删除没有被引用过的块文件
def auto_remove_unreferenced_blk(database):
    used_dict = read_json_files(os.path.join(database, "json"))
    bin_folder = os.path.join(database, "bin")
    cnt = 0
    for file in os.listdir(bin_folder):
        filepath = os.path.join(bin_folder, file)
        if used_dict.get(file) is None:
            os.remove(filepath)
            cnt += 1
            logger.info("file %s auto removed because it is not referenced" % file)
    logger.info("%d file removed" % cnt)

__all__ = [
    "create_dir",
    "input_file_and_load_into_database",
    "load_file_from_database",
    "auto_remove_unreferenced_blk"
]