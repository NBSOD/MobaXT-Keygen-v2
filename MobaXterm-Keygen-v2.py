#!/usr/bin/env python3
'''
Original Author: Double Sine
Modified By: KZ&Trae


License: GPLv3
''' 
import os
import sys
import zipfile
import argparse

VariantBase64Table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
VariantBase64Dict = {i: VariantBase64Table[i] for i in range(len(VariantBase64Table))}
VariantBase64ReverseDict = {c: i for i, c in enumerate(VariantBase64Table)}

def VariantBase64Encode(bs: bytes) -> bytes:
    result = b''
    blocks_count, left_bytes = divmod(len(bs), 3)

    for i in range(blocks_count):
        coding_int = int.from_bytes(bs[3 * i:3 * i + 3], 'little')
        block = VariantBase64Dict[coding_int & 0x3f]
        block += VariantBase64Dict[(coding_int >> 6) & 0x3f]
        block += VariantBase64Dict[(coding_int >> 12) & 0x3f]
        block += VariantBase64Dict[(coding_int >> 18) & 0x3f]
        result += block.encode()

    if left_bytes == 0:
        return result
    elif left_bytes == 1:
        coding_int = int.from_bytes(bs[3 * blocks_count:], 'little')
        block = VariantBase64Dict[coding_int & 0x3f]
        block += VariantBase64Dict[(coding_int >> 6) & 0x3f]
        result += block.encode()
        return result
    else:
        coding_int = int.from_bytes(bs[3 * blocks_count:], 'little')
        block = VariantBase64Dict[coding_int & 0x3f]
        block += VariantBase64Dict[(coding_int >> 6) & 0x3f]
        block += VariantBase64Dict[(coding_int >> 12) & 0x3f]
        result += block.encode()
        return result

def VariantBase64Decode(s: str) -> bytes:
    result = b''
    blocks_count, left_bytes = divmod(len(s), 4)

    for i in range(blocks_count):
        block = VariantBase64ReverseDict[s[4 * i]]
        block += VariantBase64ReverseDict[s[4 * i + 1]] << 6
        block += VariantBase64ReverseDict[s[4 * i + 2]] << 12
        block += VariantBase64ReverseDict[s[4 * i + 3]] << 18
        result += block.to_bytes(3, 'little')

    if left_bytes == 0:
        return result
    elif left_bytes == 2:
        block = VariantBase64ReverseDict[s[4 * blocks_count]]
        block += VariantBase64ReverseDict[s[4 * blocks_count + 1]] << 6
        result += block.to_bytes(1, 'little')
        return result
    elif left_bytes == 3:
        block = VariantBase64ReverseDict[s[4 * blocks_count]]
        block += VariantBase64ReverseDict[s[4 * blocks_count + 1]] << 6
        block += VariantBase64ReverseDict[s[4 * blocks_count + 2]] << 12
        result += block.to_bytes(2, 'little')
        return result
    else:
        raise ValueError('Invalid encoding.')

def EncryptBytes(key: int, bs: bytes) -> bytes:
    result = bytearray()
    for i in range(len(bs)):
        result.append(bs[i] ^ ((key >> 8) & 0xff))
        key = result[-1] & key | 0x482D
    return bytes(result)

def DecryptBytes(key: int, bs: bytes) -> bytes:
    result = bytearray()
    for i in range(len(bs)):
        result.append(bs[i] ^ ((key >> 8) & 0xff))
        key = bs[i] & key | 0x482D
    return bytes(result)

class LicenseType:
    Professional = 1
    Educational = 3
    Personal = 4  # 修正拼写错误

def GenerateLicense(license_type: LicenseType, count: int, username: str, major_version: int, minor_version: int, output_file: str = 'Custom.mxtpro') -> None:
    assert(count >= 0), "许可证数量不能为负数"
    
    license_string = f'{license_type}#{username}|{major_version}{minor_version}#{count}#{major_version}3{minor_version}6{minor_version}#0#0#0#'
    encoded_license = VariantBase64Encode(EncryptBytes(0x787, license_string.encode())).decode()
    
    with zipfile.ZipFile(output_file, 'w') as f:
        f.writestr('Pro.key', data=encoded_license)

def main():
    parser = argparse.ArgumentParser(description='MobaXterm 密钥生成器')
    parser.add_argument('username', help='授权用户名称')
    parser.add_argument('version', help='MobaXterm 版本号 (例如: 10.9)')
    parser.add_argument('--type', choices=['professional', 'educational', 'personal'], default='professional',
                        help='许可证类型 (默认: professional)')
    parser.add_argument('--count', type=int, default=1, help='许可证数量 (默认: 1)')
    parser.add_argument('--output', help='输出文件路径 (默认: Custom.mxtpro)')
    
    args = parser.parse_args()
    
    try:
        major_version, minor_version = args.version.split('.')[0:2]
        major_version = int(major_version)
        minor_version = int(minor_version)
    except ValueError:
        print('[*] 错误: 无效的版本格式。请使用 x.y 格式 (例如: 10.9)')
        sys.exit(1)
    
    # 映射许可证类型
    license_type_map = {
        'professional': LicenseType.Professional,
        'educational': LicenseType.Educational,
        'personal': LicenseType.Personal
    }
    license_type = license_type_map[args.type]
    
    output_file = args.output or 'Custom.mxtpro'
    
    try:
        GenerateLicense(
            license_type=license_type,
            count=args.count,
            username=args.username,
            major_version=major_version,
            minor_version=minor_version,
            output_file=output_file
        )
        
        print(f'[*] 成功!')
        print(f'[*] 生成文件: {os.path.join(os.getcwd(), output_file)}')
        print('[*] 请将生成的文件移动或复制到 MobaXterm 的安装目录。')
        print()
    except Exception as e:
        print(f'[*] 错误: 生成许可证失败: {str(e)}')
        sys.exit(1)

if __name__ == '__main__':
    main()
else:
    print('[*] 错误: 请直接运行此脚本')
    sys.exit(1)