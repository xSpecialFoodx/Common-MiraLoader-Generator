import string
import sys, os
import argparse
import shutil
import struct
import distutils.dir_util

#
# #
# # #
# # # # common mira loader generator
# # #
# #
#

class MyParser(argparse.ArgumentParser):
	def error(self, message):
		self.print_help()
		sys.stderr.write('\nerror: {0}\n'.format(message))
		sys.exit(2)


def CheckHexText(source, length, add_0x):  # returns the hex text
    source_hex = str(hex(source)[2:])
    source_hex_length = len(source_hex)
    source_hex_index = None
    source_hex_cell = None

    for source_hex_index in range(0, source_hex_length):
        source_hex_cell = source_hex[source_hex_index]

        if (source_hex_cell in string.hexdigits) is False:
            source_hex = source_hex[:source_hex_index]

            break

    result = str(source_hex.zfill(length))

    if add_0x is True:
        result = "0x" + result

    return result

Debug = False

parser = MyParser(description='files difference checker')

if Debug is False:
	parser.add_argument('--input', required=True, type=str, help='input file')
	parser.add_argument('--output', required=False, default="", type=str, help='new file')
	parser.add_argument('--dry-run', required=False, default=False, action='store_true', help='if inserted then nothing will be written to the output file')
	parser.add_argument('--verbose', required=False, default=False, action='store_true', help='detailed printing')
	parser.add_argument('--overwrite', required=False, default=False, action='store_true')
	parser.add_argument('--add-modded-to-output', required=False, default=False, action='store_true', help='if true then adds _modded to the output file name')

	if len(sys.argv) == 1:
		parser.print_usage()
		sys.exit(1)
else:
	parser.add_argument('--input', required=False, default="C:/somefolder/somefile.bin", type=str, help='input file')
	parser.add_argument('--output', required=False, default="", type=str, help='new file')
	parser.add_argument('--dry-run', required=False, default=False, action='store_true', help='if inserted then nothing will be written to the output file')
	parser.add_argument('--verbose', required=False, default=True, action='store_true', help='detailed printing')
	parser.add_argument('--overwrite', required=False, default=False, action='store_true')
	parser.add_argument('--add-modded-to-output', required=False, default=False, action='store_true', help='if true then adds _modded to the output file name')

args = parser.parse_args()

def main():
	global parser

	global args

	input_file_path = os.path.abspath(args.input).replace('\\','/')

	if not os.path.isfile(input_file_path):
		parser.error('invalid input file: {0}'.format(input_file_path))

	input_file_size = os.path.getsize(input_file_path)

	input_folder_path = os.path.dirname(input_file_path).replace('\\','/')

	if args.output == "":
		input_file_name = os.path.basename(input_file_path)
		input_file_name_length = len(input_file_name)
		input_file_name_splitted = input_file_name.split(".")
		input_file_name_splitted_amount = len(input_file_name_splitted)
		input_file_name_extension = input_file_name_splitted[input_file_name_splitted_amount - 1]
		input_file_name_extension_length = len(input_file_name_extension)
		input_file_name_without_extension = input_file_name[:input_file_name_length - input_file_name_extension_length - 1]

		output_file_name_without_extension = input_file_name_without_extension

		if args.add_modded_to_output is True:
			output_file_name_without_extension += "_modded"

		output_file_name = output_file_name_without_extension + '.' + input_file_name_extension

		if args.overwrite is True:
			output_folder_path = input_folder_path + "/backup"

			output_file_path = output_folder_path + "/" + output_file_name
		else:
			output_folder_path = input_folder_path

			if args.add_modded_to_output is False:
				output_folder_path += "/output"

			output_file_path = output_folder_path + "/" + output_file_name
	else:
		output_file_path = os.path.abspath(args.output).replace('\\','/')

		output_folder_path = os.path.dirname(output_file_path).replace('\\','/')

	if args.dry_run is False:
		distutils.dir_util.mkpath(output_folder_path)
	
	if os.path.exists(output_file_path) and not os.path.isfile(output_file_path):
		parser.error('invalid output file: {0}'.format(output_file_path))
	
	if args.dry_run is False:
		shutil.copyfile(input_file_path, output_file_path)
	
	if args.overwrite is True:
		output_file_path = input_file_path

	if args.dry_run is True:
		output_file_path_fixed = input_file_path
	else:
		output_file_path_fixed = output_file_path
	
	print(
		"Input:" + ' ' + input_file_path + "\n"
		+ "Output:" + ' ' + output_file_path + "\n"
		+ "Dry Run:" + ' ' + ("True" if args.dry_run is True else "False") + "\n"
		+ "Verbose:" + ' ' + ("True" if args.verbose is True else "False") + "\n"
		+ "Overwrite:" + ' ' + ("True" if args.overwrite is True else "False") + "\n"
		+ "Add _modded to Output:" + ' ' + ("True" if args.add_modded_to_output is True else "False")
	)

	print("")
	print('processing common mira loader file: {0}'.format(output_file_path))

	Headers = None
	Fields = None

	AddressesLength = 8#16
	SizeLength = 8#16
	ValuesLength = 8

	HeaderOffsets = (
		[
			0x00000178
			, 0x0000018e
			, 0x0000046d
			, 0x00000496
			, 0x000005c8
			, 0x00000663
			, 0x0000087b
			, 0x00000d5a
			, 0x0000106f
			, 0x000013c3
			, 0x0000174f
			, 0x00001c67
			, 0x00001d5d
			, 0x00001dd8
			, 0x00001e3b
			, 0x00001ece
			, 0x00001f31
			, 0x00001f97
			, 0x00002039
			, 0x000020d9
			, 0x0000217a
			, 0x00002259
			, 0x000022cc
			, 0x0000237f
			, 0x0000249f
			, 0x0000252d
			, 0x000025f3
			, 0x00002780
			, 0x00002829
			, 0x0000288e
			, 0x000028f3
			, 0x00002964
			, 0x00002a37
			, 0x00002ab0
			, 0x00002bf1
			, 0x00002cdd
			, 0x00002d6e
			, 0x00002ed6
			, 0x00002f75
			, 0x00003270
			, 0x0000341e
			, 0x000034f2
			, 0x000036ac
			, 0x00003717
			, 0x0000379e
			, 0x00003851
			, 0x000038c8
			, 0x00003a98
			, 0x00003ca5
			, 0x00003d65
			, 0x00003e04
			, 0x00004009
			, 0x000040bb
			, 0x00004185
			, 0x000041f1
			, 0x00004329
			, 0x00004412
			, 0x0000449f
			, 0x0000474b
			, 0x00004772
			, 0x00004780
			, 0x00004848
			, 0x000048bb
			, 0x0000499b
		]
	)  # the offsets are different between firmwares

	HeaderOffset = None

	HeaderOffsetEnd = 0x0000C000

	FooterOffsetStart = 0x00000033

	faddr = None

	struct_fmt = None
	struct_size = None

	old_struct_data = None
	old_struct_unpacked = None

	new_struct_unpacked = None
	new_struct_data = None

	old_value = None
	new_value = None

	new_value_increase = None
	new_value_decrease = None

	max_new_value_increase = 0
	max_new_value_decrease = 0

	payload_size = None
	difference = None
	
	with open(output_file_path_fixed, 'r+b') as f:
		print("")
		print("patching mira loader footer")

		struct_fmt = '<L'
		struct_size = struct.calcsize(struct_fmt)

		faddr = input_file_size - FooterOffsetStart - 1

		f.seek(faddr)

		old_struct_data = f.read(struct_size)
		old_struct_unpacked = struct.unpack(struct_fmt, old_struct_data)

		old_value = old_struct_unpacked[0]

		new_value = 0

		payload_size = old_value

		new_struct_unpacked = new_value
		new_struct_data = struct.pack(struct_fmt, new_value)

		if args.dry_run is False:
			f.seek(faddr)
			f.write(new_struct_data)

		if args.verbose is True:
			Headers = []
								
			Headers.append("Address")
			Headers.append("Old Value")
			Headers.append("New Value")

			Fields = []
			
			Fields.append(Headers[0] + ':' + ' ' + CheckHexText(faddr, AddressesLength, True))
			Fields.append(Headers[1] + ':' + ' ' + CheckHexText(old_value, ValuesLength, True))
			Fields.append(Headers[2] + ':' + ' ' + CheckHexText(new_value, ValuesLength, True))

			print('\t'.join(Fields))
			
		print("")					
		print("patched mira loader footer")

		print("")
		print("patching mira loader header")

		for HeaderOffset in HeaderOffsets:
			struct_fmt = '<L'
			struct_size = struct.calcsize(struct_fmt)

			faddr = HeaderOffset

			f.seek(faddr)

			old_struct_data = f.read(struct_size)
			old_struct_unpacked = struct.unpack(struct_fmt, old_struct_data)

			old_value = old_struct_unpacked[0]
			
			new_value_increase = 0
			new_value_decrease = 0
			
			difference = payload_size + HeaderOffsetEnd - faddr
			
			if old_value > difference:
				new_value_increase += old_value - difference

				if new_value_increase > max_new_value_increase:
					max_new_value_increase = new_value_increase
			elif old_value < difference:
				new_value_decrease += difference - old_value

				if new_value_decrease > max_new_value_decrease:
					max_new_value_decrease = new_value_decrease
				
			struct_fmt = '<HH'
			struct_size = struct.calcsize(struct_fmt)

			new_struct_unpacked = new_value_increase, new_value_decrease
			new_struct_data = struct.pack(struct_fmt, new_value_increase, new_value_decrease)

			if args.dry_run is False:
				f.seek(faddr)
				f.write(new_struct_data)

			if args.verbose is True:
				Headers = []
								
				Headers.append("Address")
				Headers.append("Old Value")
				Headers.append("New Value Increase")
				Headers.append("New Value Decrease")

				Fields = []
			
				Fields.append(Headers[0] + ':' + ' ' + CheckHexText(faddr, AddressesLength, True))
				Fields.append(Headers[1] + ':' + ' ' + CheckHexText(old_value, ValuesLength, True))
				Fields.append(Headers[2] + ':' + ' ' + CheckHexText(new_value_increase, int(ValuesLength / 2), True))
				Fields.append(Headers[3] + ':' + ' ' + CheckHexText(new_value_decrease, int(ValuesLength / 2), True))

				print('\t'.join(Fields))
			
		Headers = []
								
		Headers.append("Max New Value Increase")
		Headers.append("Max New Value Decrease")

		Fields = []
			
		Fields.append(Headers[0] + ':' + ' ' + CheckHexText(max_new_value_increase, int(ValuesLength / 2), True))
		Fields.append(Headers[1] + ':' + ' ' + CheckHexText(max_new_value_decrease, int(ValuesLength / 2), True))

		print('\t'.join(Fields))

		print("")					
		print("patched mira loader header")
		
	print("")
	print('finished processing:' + ' ' + output_file_path)

main()
