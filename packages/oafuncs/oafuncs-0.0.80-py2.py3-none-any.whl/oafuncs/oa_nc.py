#!/usr/bin/env python
# coding=utf-8
"""
Author: Liu Kun && 16031215@qq.com
Date: 2024-09-17 14:58:50
LastEditors: Liu Kun && 16031215@qq.com
LastEditTime: 2024-12-06 14:16:56
FilePath: \\Python\\My_Funcs\\OAFuncs\\oafuncs\\oa_nc.py
Description:
EditPlatform: vscode
ComputerInfo: XPS 15 9510
SystemInfo: Windows 11
Python Version: 3.11
"""

import os

import netCDF4 as nc
import numpy as np
import xarray as xr

__all__ = ["get_var", "extract5nc", "write2nc", "merge5nc", "modify_var_value", "modify_var_attr", "rename_var_or_dim", "check_ncfile"]


def get_var(file, *vars):
    """
    description: 读取nc文件中的变量
    param {file: 文件路径, *vars: 变量名}
    example: datas = get_var(file_ecm, 'h', 't', 'u', 'v')
    return {datas: 变量数据}
    """
    ds = xr.open_dataset(file)
    datas = []
    for var in vars:
        data = ds[var]
        datas.append(data)
    ds.close()
    return datas


def extract5nc(file, varname):
    """
    描述：
    1、提取nc文件中的变量
    2、将相应维度提取，建立字典
    return：返回变量及坐标字典
    参数：
    file: 文件路径
    varname: 变量名
    example: data, dimdict = extract5nc(file_ecm, 'h')
    """
    ds = xr.open_dataset(file)
    vardata = ds[varname]
    dims = vardata.dims
    dimdict = {}
    for dim in dims:
        dimdict[dim] = ds[dim].values
    ds.close()
    return np.array(vardata), dimdict


def _numpy_to_nc_type(numpy_type):
    """将NumPy数据类型映射到NetCDF数据类型"""
    numpy_to_nc = {
        "float32": "f4",
        "float64": "f8",
        "int8": "i1",
        "int16": "i2",
        "int32": "i4",
        "int64": "i8",
        "uint8": "u1",
        "uint16": "u2",
        "uint32": "u4",
        "uint64": "u8",
    }
    return numpy_to_nc.get(str(numpy_type), "f4")  # 默认使用 'float32'


def write2nc(file, data, varname, coords, mode):
    """
    description: 写入数据到nc文件
    参数：
    file: 文件路径
    data: 数据
    varname: 变量名
    coords: 坐标，字典，键为维度名称，值为坐标数据
    mode: 写入模式，'w'为写入，'a'为追加
    example: write2nc(r'test.nc', data, 'data', {'time': np.linspace(0, 120, 100), 'lev': np.linspace(0, 120, 50)}, 'a')
    """
    # 判断mode是写入还是追加
    if mode == "w":
        if os.path.exists(file):
            os.remove(file)
            print("Warning: File already exists. Deleting it.")
    elif mode == "a":
        if not os.path.exists(file):
            print("Warning: File doesn't exist. Creating a new file.")
            mode = "w"

    # 打开 NetCDF 文件
    with nc.Dataset(file, mode, format="NETCDF4") as ncfile:
        # 处理坐标
        for dim, coord_data in coords.items():
            add_coords = True
            # 判断坐标是否存在，若存在，则替换/报错
            if ncfile.dimensions:
                # 返回字典，字典、列表、元组若为空，都表示False
                if dim in ncfile.dimensions:
                    # del nc.dimensions[dim]
                    if len(coord_data) != len(ncfile.dimensions[dim]):
                        raise ValueError("Length of coordinate does not match the dimension length.")
                    else:
                        add_coords = False
                        print(f"Warning: Coordinate '{dim}' already exists. Replacing it.")
                        ncfile.variables[dim][:] = np.array(coord_data)
            if add_coords:
                # 创建新坐标
                ncfile.createDimension(dim, len(coord_data))
                ncfile.createVariable(dim, _numpy_to_nc_type(coord_data.dtype), (dim,))
                ncfile.variables[dim][:] = np.array(coord_data)

        # 判断变量是否存在，若存在，则删除原变量
        add_var = True
        if varname in ncfile.variables:
            print(f"Warning: Variable '{varname}' already exists.")
            if data.shape != ncfile.variables[varname].shape:
                raise ValueError("Shape of data does not match the variable shape.")
            else:
                # 写入数据
                ncfile.variables[varname][:] = data
                add_var = False
                print(f"Warning: Variable '{varname}' already exists. Replacing it.")

        if add_var:
            # 创建变量及其维度
            dim_names = tuple(coords.keys())  # 使用coords传入的维度名称
            ncfile.createVariable(varname, _numpy_to_nc_type(data.dtype), dim_names)
            # ncfile.createVariable('data', 'f4', ('time','lev'))

            # 写入数据
            ncfile.variables[varname][:] = data

        # 判断维度是否匹配
        if len(data.shape) != len(coords):
            raise ValueError("Number of dimensions does not match the data shape.")


def merge5nc(file_list, var_name=None, dim_name=None, target_filename=None):
    """
    批量提取 nc 文件中的变量，按照某一维度合并后写入新的 nc 文件。
    如果 var_name 是字符串，则认为是单变量；如果是列表，且只有一个元素，也是单变量；
    如果列表元素大于1，则是多变量；如果 var_name 是 None，则合并所有变量。

    参数：
    file_list：nc 文件路径列表
    var_name：要提取的变量名或变量名列表，默认为 None，表示提取所有变量
    dim_name：用于合并的维度名
    target_filename：合并后的目标文件名
    
    example: 
    merge5nc(file_list, var_name='data', dim_name='time', target_filename='merged.nc')
    merge5nc(file_list, var_name=['data1', 'data2'], dim_name='time', target_filename='merged.nc')
    merge5nc(file_list, var_name=None, dim_name='time', target_filename='merged.nc')
    """
    # 初始化变量名列表
    var_names = None

    # 判断 var_name 是单变量、多变量还是合并所有变量
    if var_name is None:
        # 获取第一个文件中的所有变量名
        ds = xr.open_dataset(file_list[0])
        var_names = list(ds.variables.keys())
        ds.close()
    elif isinstance(var_name, str):
        var_names = [var_name]
    elif isinstance(var_name, list):
        var_names = var_name
    else:
        raise ValueError("var_name must be a string, a list of strings, or None")

    # 初始化合并数据字典
    merged_data = {}

    # 遍历文件列表
    for i, file in enumerate(file_list):
        print(f"\rReading file {i + 1}/{len(file_list)}...", end="")
        ds = xr.open_dataset(file)
        for var_name in var_names:
            var = ds[var_name]
            # 如果变量包含合并维度，则合并它们
            if dim_name in var.dims:
                if var_name not in merged_data:
                    merged_data[var_name] = [var]
                else:
                    merged_data[var_name].append(var)
            # 如果变量不包含合并维度，则仅保留第一个文件中的值
            else:
                if var_name not in merged_data:
                    merged_data[var_name] = var
        ds.close()

    print("\nMerging data...")
    for var_name in merged_data:
        if isinstance(merged_data[var_name], list):
            merged_data[var_name] = xr.concat(merged_data[var_name], dim=dim_name)

    merged_data = xr.Dataset(merged_data)

    print("Writing data to file...")
    if os.path.exists(target_filename):
        print("Warning: The target file already exists.")
        print("Removing existing file...")
        os.remove(target_filename)
    merged_data.to_netcdf(target_filename)
    print(f'File "{target_filename}" has been created.')


def modify_var_value(nc_file_path, variable_name, new_value):
    """
    使用 netCDF4 库修改 NetCDF 文件中特定变量的值

    参数：
    nc_file_path (str): NetCDF 文件路径
    variable_name (str): 要修改的变量名
    new_value (numpy.ndarray): 新的变量值

    example: modify_var_value('test.nc', 'data', np.random.rand(100, 50))
    """
    try:
        # Open the NetCDF file
        dataset = nc.Dataset(nc_file_path, "r+")
        # Get the variable to be modified
        variable = dataset.variables[variable_name]
        # Modify the value of the variable
        variable[:] = new_value
        dataset.close()
        print(f"Successfully modified variable {variable_name} in {nc_file_path}.")
    except Exception as e:
        print(f"An error occurred while modifying variable {variable_name} in {nc_file_path}: {e}")


def modify_var_attr(nc_file_path, variable_name, attribute_name, attribute_value):
    """
    使用 netCDF4 库添加或修改 NetCDF 文件中特定变量的属性。

    参数：
    nc_file_path (str): NetCDF 文件路径
    variable_name (str): 要操作的变量名
    attribute_name (str): 属性名
    attribute_value (任意类型): 属性值
    example: modify_var_attr('test.nc', 'data', 'long_name', 'This is a test variable.')
    """
    try:
        ds = nc.Dataset(nc_file_path, "r+")
        if variable_name not in ds.variables:
            raise ValueError(f"Variable '{variable_name}' not found in the NetCDF file.")

        variable = ds.variables[variable_name]
        if attribute_name in variable.ncattrs():
            print(f"Warning: Attribute '{attribute_name}' already exists. Replacing it.")
            variable.setncattr(attribute_name, attribute_value)
        else:
            print(f"Adding attribute '{attribute_name}'...")
            variable.setncattr(attribute_name, attribute_value)

        ds.close()
    except Exception as e:
        raise RuntimeError(f"An error occurred: {e}")


def rename_var_or_dim(ncfile_path, old_name, new_name):
    """
    Rename a variable and/or dimension in a NetCDF file.

    Parameters:
    ncfile_path (str): The path to the NetCDF file.
    old_name (str): The name of the variable or dimension to be renamed.
    new_name (str): The new name for the variable or dimension.

    example: rename_var_or_dim('test.nc', 'time', 'ocean_time')
    """
    try:
        with nc.Dataset(ncfile_path, "r+") as dataset:
            # If the old name is not found as a variable or dimension, print a message
            if old_name not in dataset.variables and old_name not in dataset.dimensions:
                print(f"Variable or dimension {old_name} not found in the file.")

            # Attempt to rename the variable
            if old_name in dataset.variables:
                dataset.renameVariable(old_name, new_name)
                print(f"Successfully renamed variable {old_name} to {new_name}.")

            # Attempt to rename the dimension
            if old_name in dataset.dimensions:
                # Check if the new dimension name already exists
                if new_name in dataset.dimensions:
                    raise ValueError(f"Dimension name {new_name} already exists in the file.")
                dataset.renameDimension(old_name, new_name)
                print(f"Successfully renamed dimension {old_name} to {new_name}.")

    except Exception as e:
        print(f"An error occurred: {e}")


def check_ncfile(ncfile, if_delete=False):
    if not os.path.exists(ncfile):
        return False

    try:
        with nc.Dataset(ncfile, "r") as f:
            # 确保f被使用，这里我们检查文件中变量的数量
            if len(f.variables) > 0:
                return True
            else:
                # 如果没有变量，我们可以认为文件是损坏的
                raise ValueError("File is empty or corrupted.")
    except OSError as e:
        # 捕获文件打开时可能发生的OSError
        print(f"An error occurred while opening the file: {e}")
        if if_delete:
            os.remove(ncfile)
            print(f"File {ncfile} has been deleted.")
        return False
    except Exception as e:
        # 捕获其他可能的异常
        print(f"An unexpected error occurred: {e}")
        if if_delete:
            os.remove(ncfile)
            print(f"File {ncfile} has been deleted.")
        return False


if __name__ == "__main__":
    data = np.random.rand(100, 50)
    write2nc(r"test.nc", data, "data", {"time": np.linspace(0, 120, 100), "lev": np.linspace(0, 120, 50)}, "a")
