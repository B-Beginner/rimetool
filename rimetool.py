import argparse
import vcf_to_dict

if __name__ == '__main__':


    parser = argparse.ArgumentParser(description='rime输入法相关工具 https://github.com/whitewatercn/rimetool')
    parser.add_argument('method', type=str, help='vcf：转换.vcf通讯录文件为rime词库 ')
    # parser.add_argument('url', type=str, help='视频url，如果是获取整个系列，提供系列中任意一集视频的url即可')
    # parser.add_argument('-q', type=int, default=0, help='视频画面质量，默认0为最高画质，越大画质越低，超出范围时自动选最低画质')
    # parser.add_argument('-max_con', type=int, default=5, help='控制最大同时下载的视频数量，理论上网络带宽越高可以设的越高')
    # parser.add_argument('-cookie', type=str, default='', help='有条件的用户可以提供大会员的SESSDATA来下载会员视频')
    # parser.add_argument('-dir', type=str, default='videos', help='文件的下载目录，默认当前路径下的videos文件夹下，不存在会自动创建')

	
    asyncio.run(main(parser.parse_args()))


	
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('command', choices=['vcf', 'test'])
	args = parser.parse_args()
	
	if args.command == 'vcf':
		vcf_to_dict.main()
	elif args.command == 'test':
		print('test')

if __name__ == "__main__":
    main()