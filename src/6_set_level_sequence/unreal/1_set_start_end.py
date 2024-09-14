import unreal

DURATION = 7684

# 指定要遍历的文件夹路径
folder_path = "/Game/Sequence/DivSequence/Sng026"  # 替换为您的文件夹路径

# 获取资产库
asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()

# 获取文件夹中的所有资产数据
asset_data_list = asset_registry.get_assets_by_path(folder_path, recursive=True)

# 遍历并打印每个资产的名称和路径
for asset_data in asset_data_list:
    asset_path = asset_data.object_path
    level_sequence = unreal.LevelSequence.cast(unreal.load_asset(asset_path))
    o_start = level_sequence.get_playback_start()

    o_end = o_start+DURATION
    level_sequence.set_playback_end(o_end)
