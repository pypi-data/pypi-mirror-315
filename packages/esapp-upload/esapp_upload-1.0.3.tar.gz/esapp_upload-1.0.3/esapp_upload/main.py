# -*- coding: utf-8 -*-
import os
import zipfile
import argparse
import esapp_upload.upload

def zip_directory(folder_path, output_path):
    """
    压缩指定目录为ZIP文件。

    :param folder_path: 要压缩的目录路径
    :param output_path: 输出的ZIP文件路径
    """
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=folder_path)
                zipf.write(file_path, arcname)

def main():
    print("欢迎使用压缩目录并上传到ES应用服务器脚本！")
    print("请确保已安装Python和zipfile库。")
    print("请输入参数：")
    print("参数说明：")
    print("--dir: 要压缩的目录路径")
    print("--zipfile: 输出的ZIP文件路径")
    print("--package_name: 包名称")
    print("--version: 版本号")
    print("--is_production: 是否为生产环境，默认为False")
    print("--refresh: 刷新标志，默认为0")
    print("--remark: 备注，默认为空")
    print("设置测试和正式环境变量 ESAPP_TEST_TOKEN  ESAPP_PROP_TOKEN")
    parser = argparse.ArgumentParser(description='压缩目录并上传到ES应用服务器')
    parser.add_argument('--dir', type=str, required=True, help='要压缩的目录路径')
    parser.add_argument('--zipfile', type=str, required=True, help='输出的ZIP文件路径')
    parser.add_argument('--package_name', type=str, required=True, help='包名称')
    parser.add_argument('--version', type=str, required=True, help='版本号')
    parser.add_argument('--is_production', action='store_true', help='是否为生产环境')
    parser.add_argument('--refresh', type=str, default='0', help='刷新标志')
    parser.add_argument('--remark', type=str, default='', help='备注')

    args = parser.parse_args()

    zip_directory(args.dir, args.zipfile)
    print(f"目录 {args.dir} 已成功压缩为 {args.zipfile}")
    
    esapp_upload.upload_es_app(
        package_name=args.package_name,
        version=args.version,
        file_path=args.zipfile,
        is_production=args.is_production,
        refresh=args.refresh,
        remark=args.remark
    )
### 示例 python3 main.py --dir android --zipfile android.zip --package_name es.huan.cece.com --version 1.0.3  
### 设置
if __name__ == "__main__":
    main()
