import argparse

from . import create_dir, input_file_and_load_into_database, load_file_from_database, auto_remove_unreferenced_blk
from .mylog import logger

# 创建一个解析器
parser = argparse.ArgumentParser(description="")

# 添加参数
parser.add_argument('-d', '--data'  , type=str, required=True, help='the position of root dir of the database')
parser.add_argument('-o', '--output', type=str, help='generate a full file from database')
parser.add_argument('-s', '--select', type=str, help='select a file to output with hash value')
parser.add_argument('-i', '--input' , type=str, help='try to save a file into database')
parser.add_argument('-r', '--remove' , action='store_true', help='remove unreferenced block file')

# 解析命令行参数
args = parser.parse_args().__dict__
logger.debug(str(args))

# 读取数据库文件位置, 创建必要的工作目录
database_folder = args["data"]
create_dir(database_folder)

# 记录哪些命令被执行了
input_command = False
output_command = False
remove_command = False

# 执行将文件载入数据库的逻辑
if args.get("input") is not None:
    filepath = args.get("input")
    logger.info("input command triggered.")
    input_file_and_load_into_database(filepath, database_folder)
    input_command = True

# 执行将数据库中文件读出来的逻辑
if args.get("output") is not None and args.get("select") is not None:
    selectjson = args.get("select")
    outputpath = args.get("output")
    logger.info("output command triggered")
    load_file_from_database(outputpath, database_folder, selectjson)
    output_command = True

# 删除没有被引用过的数据块
if args.get("remove") is True:
    logger.info("auto remove triggered")
    auto_remove_unreferenced_blk(database_folder)
    remove_command = True

# 什么都没有做，也稍微写一个日志
if not input_command and not output_command and not remove_command:
    logger.info("no command triggered")