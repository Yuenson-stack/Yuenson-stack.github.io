import os 

class FileSystem(object):
    
    '''
    作者：Samson
    日期：2023-10-11
    描述：一个文件工具，可以通过遍历文件系统的方式执行如下操作：
         1. 打印并下载指定目录的文件树 
         2. 统计并下载指定目录的文件大小
         3. 批量删除指定目录的指定文件类型
    使用方法：
         python FileSystem.py -r/--root rootdirectory -m/--mdethod [tree,dtree,size,dsize,del] 
                             [--ftype] file type [--subdir] sub-directory [--re] recursion or not 
                             
    参数说明： 1. -r/--root 指定需要处理的文件系统的根目录
             2. -m/--method 需要进行的文件系统操作
                    tree：打印文件树
                    dtree：下载文件树
                    size：遍历统计文件目录大小
                    dsize：下载文件目录大小结果
                    del：删除指定文件路径下的指定种类的文件
             3.ftype：需要删除的文件种类，当-m/--method为del时，该参数必须
             4.subdir：删除文件时起始的文件夹路径，默认不输入时与-r/--root 相同
             5.re：删除文件的方式，默认不输入时为非递归删除，布尔型。
    '''
    
    
    def __init__(self,root):
        
        '''
        初始化所要操作的工具对象，只需要传入所需要让工具处理的目录即可  
        '''
        
        self.root = root 
        self.__file_tree_str = '' 
        self.__file_tree_str_with_size = '' 
        self.__total_size = 0
        self.__size_list = []
        self.__vp_list = [] 
        
        
    def __print_file_tree(self,root,level=0,vp_list=[]):
        
        if level==0:
            self.__file_tree_str += (root+'\n')
            
        file_list = os.listdir(root)
        n = len(file_list)
        
        for k,file in enumerate(file_list):  
            
            join_sep = '---' if not (k == n-1) else '___'
            sub_path = os.path.join(root,file)
            
            temp_item = ''
            for i in vp_list:
                temp_item += ('|' if i else ' ')+'    ' 
            temp_item += '|'+join_sep+' '+file
            self.__size_list.append(os.path.getsize(sub_path))

            
            self.__file_tree_str += (temp_item+'\n')
            
            if os.path.isdir(sub_path) and k!= n-1:
                self.__vp_list.append(True)
                self.__print_file_tree(sub_path,level=level+1,vp_list=self.__vp_list)
            elif os.path.isdir(sub_path) and k==n-1:
                self.__vp_list.append(False)
                self.__print_file_tree(sub_path,level=level+1,vp_list=self.__vp_list)
            
        if len(self.__vp_list):
            self.__vp_list.pop()
            
            
    def print_file_tree(self):
        
        print(self.__str__())
    
    
    def download_file_tree(self):
        
        with open(self.root+' tree.txt','w') as f:
            
            f.write(self.__str__())
            
                
    def __str__(self):
    
        if self.__file_tree_str == '':
            self.__print_file_tree(root=self.root)
        
        return self.__file_tree_str
    
            
    def file_size(self):
        
        temp_list = self.__str__().split('\n')
        temp_list = temp_list[:-1]
        
        max_char = len(temp_list[0])
        
        for line in temp_list:
            
            if len(line) > max_char: 
                max_char = len(line)  
                
        for index in range(len(temp_list)):
            
            if index >0:
                char_diff = max_char-len(temp_list[index])
                temp_list[index] += (char_diff+8)*' '+ str(int(self.__size_list[index-1]/1024)) + ' KB\n'
                
                
        self.__total_size = int(sum(self.__size_list))
        
        temp_list[0] += (max_char-len(temp_list[0])+8)*' '+str(int(self.__total_size/1024)) + ' KB\n'
        
        self.__file_tree_str_with_size = ''.join(temp_list)
        print(self.__file_tree_str_with_size)
        
        
    def download_file_size(self):
        
        if self.__file_tree_str_with_size == '':
            self.file_size() 
            
        with open(self.root + ' file size.txt','w') as f:
            f.write(self.__file_tree_str_with_size)        
                
                
    def del_file(self,file_type,dir_path=None,recursion=False):
        
        '''
        批量删所需处理文件系统中的某一类文件,默认是非递归的
        '''
        import send2trash
        
        if not dir_path:
            dir_path = self.root
     
        for file in os.listdir(dir_path):
            
            sub_path = os.path.join(dir_path,file)
            
            if os.path.isfile(sub_path) and file.endswith(file_type):
                send2trash.send2trash(sub_path)
                
            if os.path.isdir(sub_path) and recursion:
                self.del_file(dir_path=sub_path,file_type = file_type,recursion = recursion) 
                
                
                
if __name__ == '__main__':
    
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-r','--root',type=str, required=True,help='root directory')
    parser.add_argument('-m','--method',type=str, required=True,help = 'file system method')
    parser.add_argument('--subdir',type=str, required=False)
    parser.add_argument('--ftype',type=str, required=False)
    parser.add_argument('--re',type=bool, required=False)
    args = parser.parse_args()
    
    fs = FileSystem(args.root)
    
    if args.method == 'dtree':
        fs.download_file_tree()
    elif args.method == 'tree':
        fs.print_file_tree()
    elif args.method == 'dsize':
        fs.download_file_size()
    elif args.method == 'size':
        fs.file_size()
    elif args.method == 'del':
        if not args.ftype:
            raise Exception('Please entre file type you want to delete')
        else:
            fs.del_file(dir_path=args.subdir,file_type=args.ftype,recursion=args.re)