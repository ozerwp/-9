"""
图书数据访问类
处理图书数据的增删改查操作
"""
from datetime import datetime
from typing import List, Optional
from book_management.models.book import Book


class BookRepository:
    """图书数据访问类
    
    方法:
        save: 保存图书
        find_by_id: 根据ID查找图书
        find_by_isbn: 根据ISBN查找图书
        find_by_params: 根据参数查找图书
        update: 更新图书
        delete: 删除图书
        find_all: 获取所有图书
    """
    
    def __init__(self):
        """初始化图书数据访问对象
        
        创建内存存储来模拟数据库
        """
        self._books: List[Book] = []
        self._next_id = 1
    
    def save(self, book: Book) -> Book:
        """保存图书
        
        参数:
            book: 图书对象
            
        返回:
            保存后的图书对象
        """
        if book.book_id is None or book.book_id == 0:
            # 新图书，分配ID
            book.book_id = self._next_id
            self._next_id += 1
            self._books.append(book)
        else:
            # 更新现有图书
            for i, existing_book in enumerate(self._books):
                if existing_book.book_id == book.book_id:
                    self._books[i] = book
                    break
        return book
    
    def find_by_id(self, book_id: int) -> Optional[Book]:
        """根据ID查找图书
        
        参数:
            book_id: 图书ID
            
        返回:
            图书对象，如果找不到返回None
        """
        for book in self._books:
            if book.book_id == book_id:
                return book
        return None
    
    def find_by_isbn(self, isbn: str) -> Optional[Book]:
        """根据ISBN查找图书
        
        参数:
            isbn: ISBN
            
        返回:
            图书对象，如果找不到返回None
        """
        for book in self._books:
            if book.isbn == isbn:
                return book
        return None
    
    def find_by_params(self, title: Optional[str] = None, 
                      author: Optional[str] = None, 
                      category_id: Optional[int] = None) -> List[Book]:
        """根据参数查找图书
        
        参数:
            title: 书名（模糊匹配）
            author: 作者（模糊匹配）
            category_id: 分类ID
            
        返回:
            图书列表
        """
        result = []
        for book in self._books:
            match = True
            
            if title and title.lower() not in book.title.lower():
                match = False
            if author and author.lower() not in book.author.lower():
                match = False
            if category_id and book.category_id != category_id:
                match = False
            
            if match:
                result.append(book)
        
        return result
    
    def update(self, book: Book) -> bool:
        """更新图书
        
        参数:
            book: 图书对象
            
        返回:
            更新是否成功
        """
        for i, existing_book in enumerate(self._books):
            if existing_book.book_id == book.book_id:
                self._books[i] = book
                return True
        return False
    
    def delete(self, book_id: int) -> bool:
        """删除图书
        
        参数:
            book_id: 图书ID
            
        返回:
            删除是否成功
        """
        for i, book in enumerate(self._books):
            if book.book_id == book_id:
                del self._books[i]
                return True
        return False
    
    def find_all(self) -> List[Book]:
        """获取所有图书
        
        返回:
            图书列表
        """
        return self._books.copy()
