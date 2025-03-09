import os

subdirectories = []


def list_subdirectories(prefix, directory):
	try:
        # 获取目录下的所有文件和子目录
		entries = os.listdir(directory)
        
        # 遍历所有条目，将子目录添加到列表中
		for entry in entries:
			if entry[0] == ".":
				continue
			full_path = os.path.join(directory, entry)
			if os.path.isdir(full_path):
				new_prefix = prefix + "/" + entry
				subdirectories.append(new_prefix)
				list_subdirectories(new_prefix, full_path)
	except FileNotFoundError:
		print(f"Directory '{directory}' not found.")
		return []
	except PermissionError:
		print(f"Permission denied for directory '{directory}'.")
		return []


if __name__ == "__main__":
	while True:
		directory = input("Enter the directory path: ")
		if directory == "q":
			exit()
		list_subdirectories("${CMAKE_SOURCE_DIR}", directory)
		
		with open(directory + "\\" + "CMakeLists.txt", "w") as f:
			f.write("CMAKE_MINIMUM_REQUIRED(VERSION 3.14)\n")
			f.write("PROJECT(BMCx VERSION 1.0 LANGUAGES CXX C)\n")
			
			f.write("\n")

			f.write("SET(INCLUDE_LIST\n")
			f.write("	${CMAKE_SOURCE_DIR}\n")
			for subdir in subdirectories:
				f.write("	" + subdir + "\n")
			f.write(")\n")
			f.write("INCLUDE_DIRECTORIES(${INCLUDE_LIST})\n")
			
			f.write("\n")

			f.write("AUX_SOURCE_DIRECTORY(${CMAKE_SOURCE_DIR} SRC_LIST)\n")
			for subdir in subdirectories:
				f.write("AUX_SOURCE_DIRECTORY(" + subdir + " SRC_LIST)\n")
			f.write("ADD_LIBRARY(BMCx SHARED ${SRC_LIST})\n")
		
		print (f"生成CMake文件完成，按 q 退出\n")
		