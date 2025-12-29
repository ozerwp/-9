"""
图书实体类
定义图书的基本属性和方法
"""
from datetime import datetime
from typing import Optional


class Book:
    """图书类
    
    属性:
        book_id: 图书ID
        isbn: ISBN
        title: 书名
        author: 作者
        publisher: 出版社
        publish_date: 出版日期
        category_id: 分类ID
        price: 价格
        total_quantity: 总数量
        available_quantity: 可借数量
        create_time: 创建时间
        update_time: 更新时间
    
    方法:
        get_status: 获取图书状态
        update_quantity: 更新图书数量
        to_dict: 转换为字典
    """
    
    def __init__(self, book_id: int, isbn: str, title: str, author: str, 
                 publisher: str, publish_date: datetime, category_id: int, 
                 price: float, total_quantity: int):
        """初始化图书对象
        
        参数:
            book_id: 图书ID
            isbn: ISBN
            title: 书名
            author: 作者
            publisher: 出版社
            publish_date: 出版日期
            category_id: 分类ID
            price: 价格
            total_quantity: 总数量
        """
        self.book_id = book_id
        self.isbn = isbn
        self.title = title
        self.author = author
        self.publisher = publisher
        self.publish_date = publish_date
        self.category_id = category_id
        self.price = price
        self.total_quantity = total_quantity
        self.available_quantity = total_quantity
        self.create_time = datetime.now()
        self.update_time = datetime.now()
    
    def get_status(self) -> str:
        """获取图书状态
        
        返回:
            图书状态："可借"或"已借出"
        """
        if self.available_quantity > 0:
            return "可借"
        return "已借出"
    
    def update_quantity(self, change: int) -> bool:
        """更新图书数量
        
        参数:
            change: 数量变化值（正数表示增加，负数表示减少）
            
        返回:
            更新是否成功
        """
        new_quantity = self.available_quantity + change
        if new_quantity >= 0 and new_quantity <= self.total_quantity:
            self.available_quantity = new_quantity
            self.update_time = datetime.now()
            return True
        return False
    
    def to_dict(self) -> dict:
        """转换为字典
        
        返回:
            图书信息字典
        """
        return {
            'book_id': self.book_id,
            'isbn': self.isbn,
            'title': self.title,
            'author': self.author,
            'publisher': self.publisher,
            'publish_date': self.publish_date.strftime('%Y-%m-%d'),
            'category_id': self.category_id,
            'price': self.price,
            'total_quantity': self.total_quantity,
            'available_quantity': self.available_quantity,
            'status': self.get_status(),
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def __str__(self) -> str:
        """字符串表示
        
        返回:
            图书信息字符串
        """
        return f"Book(book_id={self.book_id}, title='{self.title}', author='{self.author}', status='{self.get_status()}')"
