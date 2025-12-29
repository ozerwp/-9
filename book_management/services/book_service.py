"""
图书服务类
处理图书相关的业务逻辑
"""
from datetime import datetime
from typing import List, Optional
from book_management.models.book import Book
from book_management.repositories.book_repository import BookRepository


class BookService:
    """图书服务类
    
    方法:
        add_book: 添加图书
        get_book_by_id: 根据ID获取图书
        get_book_by_isbn: 根据ISBN获取图书
        search_books: 搜索图书
        update_book: 更新图书
        delete_book: 删除图书
        get_all_books: 获取所有图书
        borrow_book: 借阅图书
        return_book: 归还图书
    """
    
    def __init__(self):
        """初始化图书服务对象
        
        创建图书数据访问对象
        """
        self._book_repo = BookRepository()
    
    def add_book(self, isbn: str, title: str, author: str, 
                publisher: str, publish_date: datetime, 
                category_id: int, price: float, 
                total_quantity: int) -> Book:
        """添加图书
        
        参数:
            isbn: ISBN
            title: 书名
            author: 作者
            publisher: 出版社
            publish_date: 出版日期
            category_id: 分类ID
            price: 价格
            total_quantity: 总数量
            
        返回:
            添加的图书对象
            
        异常:
            ValueError: ISBN已存在
        """
        # 检查ISBN是否已存在
        existing_book = self._book_repo.find_by_isbn(isbn)
        if existing_book:
            raise ValueError(f"ISBN {isbn} 已存在")
        
        # 创建图书对象
        book = Book(
            book_id=0,  # 0表示新图书，将由仓库分配ID
            isbn=isbn,
            title=title,
            author=author,
            publisher=publisher,
            publish_date=publish_date,
            category_id=category_id,
            price=price,
            total_quantity=total_quantity
        )
        
        # 保存图书
        return self._book_repo.save(book)
    
    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """根据ID获取图书
        
        参数:
            book_id: 图书ID
            
        返回:
            图书对象，如果找不到返回None
        """
        return self._book_repo.find_by_id(book_id)
    
    def get_book_by_isbn(self, isbn: str) -> Optional[Book]:
        """根据ISBN获取图书
        
        参数:
            isbn: ISBN
            
        返回:
            图书对象，如果找不到返回None
        """
        return self._book_repo.find_by_isbn(isbn)
    
    def search_books(self, title: Optional[str] = None, 
                    author: Optional[str] = None, 
                    category_id: Optional[int] = None) -> List[Book]:
        """搜索图书
        
        参数:
            title: 书名（模糊匹配）
            author: 作者（模糊匹配）
            category_id: 分类ID
            
        返回:
            符合条件的图书列表
        """
        return self._book_repo.find_by_params(title, author, category_id)
    
    def get_all_books(self) -> List[Book]:
        """获取所有图书
        
        返回:
            所有图书的列表
        """
        return self._book_repo.find_all()
    
    def update_book(self, book_id: int, **kwargs) -> Optional[Book]:
        """更新图书
        
        参数:
            book_id: 图书ID
            kwargs: 要更新的字段
            
        返回:
            更新后的图书对象，如果找不到返回None
        """
        book = self._book_repo.find_by_id(book_id)
        if not book:
            return None
        
        # 更新字段
        for key, value in kwargs.items():
            if hasattr(book, key):
                setattr(book, key, value)
        
        return book
    
    def delete_book(self, book_id: int) -> bool:
        """删除图书
        
        参数:
            book_id: 图书ID
            
        返回:
            删除是否成功
        """
        return self._book_repo.delete(book_id)
    
    def borrow_book(self, book_id: int) -> bool:
        """借阅图书
        
        参数:
            book_id: 图书ID
            
        返回:
            借阅是否成功
        """
        book = self._book_repo.find_by_id(book_id)
        if not book:
            return False
        
        # 检查图书是否可借
        if book.available_quantity <= 0:
            return False
        
        # 更新图书数量
        return book.update_quantity(-1)
    
    def return_book(self, book_id: int) -> bool:
        """归还图书
        
        参数:
            book_id: 图书ID
            
        返回:
            归还是否成功
        """
        book = self._book_repo.find_by_id(book_id)
        if not book:
            return False
        
        # 检查图书是否可以归还
        if book.available_quantity >= book.total_quantity:
            return False
        
        # 更新图书数量
        return book.update_quantity(1)
