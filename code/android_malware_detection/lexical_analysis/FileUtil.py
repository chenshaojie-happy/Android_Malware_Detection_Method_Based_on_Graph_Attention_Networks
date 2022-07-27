# coding=utf-8


'''
 * 文件操作
 * @author zhangyu
'''

class FileUtil:

    '''
     * 文件读取到缓冲区
     * @param buffer 缓冲区
     * @param fileSrc 文件路径
     * @return true : success
     *            false : filed
    '''

    def readFile(file_in):
        buffer = ''
        try:
            # for line in file_in.read():
            #     buffer += line
            # for ch in file_in.read():
            #     buffer += chr(ch)
            buffer = str(file_in.read().decode('utf-8'))
            return buffer, True
        except Exception as e:
            print(e)
        return buffer, False

    '''
     * 追加方式写文件
     * @param args    需要写入字符串
     * @return    true : success
     *            false : filed
    '''
#     public static boolean writeFile(String filepath,String args) {
#         try {
#             File file = new File(filepath);
#             if (!file.exists()) {
#                 file.createNewFile();
#             }
#             FileWriter fw = new FileWriter(file.getAbsoluteFile(),true);
#             BufferedWriter bw = new BufferedWriter(fw);
#             bw.write(args);
#             bw.close();
#             return true;
#         } catch (IOException e) {
#             e.printStackTrace();
#             return true;
#         }
#     }
#     /**
#      * 清空文件
#      */
#     public static boolean clearFile(String filepath) {
#         try {
#             File file = new File(filepath);
#             if (!file.exists()) {
#                 file.createNewFile();
#             }
#             FileWriter fw = new FileWriter(file.getAbsoluteFile());
#             BufferedWriter bw = new BufferedWriter(fw);
#             bw.write("");
#             bw.close();
#             return true;
#         } catch (IOException e) {
#             e.printStackTrace();
#             return true;
#         }
#     }
# }
