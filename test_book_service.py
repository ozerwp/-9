"""
图书服务单元测试
使用pytest框架测试图书服务的各种功能
"""
import pytest
from datetime import datetime
from book_management.services.book_service import BookService


class TestBookService:
    """图书服务单元测试类"""
    
    def setup_method(self):
        """每个测试方法执行前的设置
        
        创建图书服务对象和测试数据
        """
        self.book_service = BookService()
        self.test_book_data = {
            "isbn": "9787115546081",
            "title": "Python编程：从入门到实践",
            "author": "Eric Matthes",
            "publisher": "人民邮电出版社",
            "publish_date": datetime(2020, 1, 1),
            "category_id": 1,
            "price": 89.0,
            "total_quantity": 5
        }
    
    def test_add_book_success(self):
        """测试添加图书成功场景"""
        # 执行添加图书操作
        book = self.book_service.add_book(**self.test_book_data)
        
        # 验证结果
        assert book is not None
        assert book.isbn == self.test_book_data["isbn"]
        assert book.title == self.test_book_data["title"]
        assert book.author == self.test_book_data["author"]
        assert book.book_id > 0
        
    def test_add_book_duplicate_isbn(self):
        """测试添加图书失败场景：ISBN已存在"""
        # 先添加一本图书
        self.book_service.add_book(**self.test_book_data)
        
        # 再次添加同一ISBN的图书，预期抛出ValueError
        with pytest.raises(ValueError) as excinfo:
            self.book_service.add_book(**self.test_book_data)
        
        # 验证错误信息
        assert f"ISBN {self.test_book_data['isbn']} 已存在" in str(excinfo.value)
    
    def test_get_book_by_id_success(self):
        """测试根据ID获取图书成功场景"""
        # 先添加一本图书
        added_book = self.book_service.add_book(**self.test_book_data)
        
        # 根据ID获取图书
        retrieved_book = self.book_service.get_book_by_id(added_book.book_id)
        
        # 验证结果
        assert retrieved_book is not None
        assert retrieved_book.book_id == added_book.book_id
        assert retrieved_book.title == added_book.title
    
    def test_get_book_by_id_not_found(self):
        """测试根据ID获取图书失败场景：图书不存在"""
        # 尝试获取不存在的图书ID
        retrieved_book = self.book_service.get_book_by_id(999)
        
        # 验证结果
        assert retrieved_book is None
    
    def test_get_book_by_isbn_success(self):
        """测试根据ISBN获取图书成功场景"""
        # 先添加一本图书
        self.book_service.add_book(**self.test_book_data)
        
        # 根据ISBN获取图书
        retrieved_book = self.book_service.get_book_by_isbn(self.test_book_data["isbn"])
        
        # 验证结果
        assert retrieved_book is not None
        assert retrieved_book.isbn == self.test_book_data["isbn"]
    
    def test_get_book_by_isbn_not_found(self):
        """测试根据ISBN获取图书失败场景：图书不存在"""
        # 尝试获取不存在的ISBN
        retrieved_book = self.book_service.get_book_by_isbn("9999999999999")
        
        # 验证结果
        assert retrieved_book is None
    
    def test_get_all_books(self):
        """测试获取所有图书场景"""
        # 初始状态应该没有图书
        books = self.book_service.get_all_books()
        assert len(books) == 0
        
        # 添加一本图书
        self.book_service.add_book(**self.test_book_data)
        
        # 验证获取到一本图书
        books = self.book_service.get_all_books()
        assert len(books) == 1
        
        # 添加第二本图书
        book_data2 = self.test_book_data.copy()
        book_data2["isbn"] = "9787111647813"
        book_data2["title"] = "流畅的Python"
        self.book_service.add_book(**book_data2)
        
        # 验证获取到两本图书
        books = self.book_service.get_all_books()
        assert len(books) == 2
    
    def test_search_books_by_title(self):
        """测试根据书名搜索图书场景"""
        # 添加两本不同书名的图书
        self.book_service.add_book(**self.test_book_data)
        
        book_data2 = self.test_book_data.copy()
        book_data2["isbn"] = "9787111647813"
        book_data2["title"] = "流畅的Python"
        self.book_service.add_book(**book_data2)
        
        # 根据书名搜索
        result = self.book_service.search_books(title="Python")
        
        # 验证结果
        assert len(result) == 2  # 两本书名都包含"Python"
        
        result = self.book_service.search_books(title="流畅")
        assert len(result) == 1  # 只有一本包含"流畅"
    
    def test_search_books_by_author(self):
        """测试根据作者搜索图书场景"""
        # 添加两本不同作者的图书
        self.book_service.add_book(**self.test_book_data)
        
        book_data2 = self.test_book_data.copy()
        book_data2["isbn"] = "9787111647813"
        book_data2["title"] = "流畅的Python"
        book_data2["author"] = "Luciano Ramalho"
        self.book_service.add_book(**book_data2)
        
        # 根据作者搜索
        result = self.book_service.search_books(author="Eric")
        
        # 验证结果
        assert len(result) == 1
        assert result[0].author == "Eric Matthes"
    
    def test_update_book_success(self):
        """测试更新图书成功场景"""
        # 先添加一本图书
        added_book = self.book_service.add_book(**self.test_book_data)
        
        # 更新图书信息
        updated_book = self.book_service.update_book(
            book_id=added_book.book_id,
            price=99.0,  # 更新价格
            title="Python编程：从入门到实践（第2版）"  # 更新书名
        )
        
        # 验证结果
        assert updated_book is not None
        assert updated_book.price == 99.0
        assert updated_book.title == "Python编程：从入门到实践（第2版）"
    
    def test_update_book_not_found(self):
        """测试更新图书失败场景：图书不存在"""
        # 尝试更新不存在的图书
        updated_book = self.book_service.update_book(
            book_id=999,
            price=99.0
        )
        
        # 验证结果
        assert updated_book is None
    
    def test_delete_book_success(self):
        """测试删除图书成功场景"""
        # 先添加一本图书
        added_book = self.book_service.add_book(**self.test_book_data)
        
        # 删除图书
        result = self.book_service.delete_book(added_book.book_id)
        
        # 验证结果
        assert result is True
        
        # 验证图书已被删除
        deleted_book = self.book_service.get_book_by_id(added_book.book_id)
        assert deleted_book is None
    
    def test_delete_book_not_found(self):
        """测试删除图书失败场景：图书不存在"""
        # 尝试删除不存在的图书
        result = self.book_service.delete_book(999)
        
        # 验证结果
        assert result is False
    
    def test_borrow_book_success(self):
        """测试借阅图书成功场景"""
        # 先添加一本图书
        added_book = self.book_service.add_book(**self.test_book_data)
        
        # 借阅图书
        result = self.book_service.borrow_book(added_book.book_id)
        
        # 验证结果
        assert result is True
        
        # 验证图书可借数量减少
        borrowed_book = self.book_service.get_book_by_id(added_book.book_id)
        assert borrowed_book.available_quantity == self.test_book_data["total_quantity"] - 1
    
    def test_borrow_book_not_found(self):
        """测试借阅图书失败场景：图书不存在"""
        # 尝试借阅不存在的图书
        result = self.book_service.borrow_book(999)
        
        # 验证结果
        assert result is False
    
    def test_borrow_book_unavailable(self):
        """测试借阅图书失败场景：图书已借出"""
        # 先添加一本图书，数量为1
        test_data = self.test_book_data.copy()
        test_data["total_quantity"] = 1
        added_book = self.book_service.add_book(**test_data)
        
        # 第一次借阅成功
        result1 = self.book_service.borrow_book(added_book.book_id)
        assert result1 is True
        
        # 第二次借阅失败，因为图书已借出
        result2 = self.book_service.borrow_book(added_book.book_id)
        assert result2 is False
    
    def test_return_book_success(self):
        """测试归还图书成功场景"""
        # 先添加一本图书
        added_book = self.book_service.add_book(**self.test_book_data)
        
        # 先借阅图书
        self.book_service.borrow_book(added_book.book_id)
        
        # 归还图书
        result = self.book_service.return_book(added_book.book_id)
        
        # 验证结果
        assert result is True
        
        # 验证图书可借数量增加
        returned_book = self.book_service.get_book_by_id(added_book.book_id)
        assert returned_book.available_quantity == self.test_book_data["total_quantity"]
    
    def test_return_book_not_found(self):
        """测试归还图书失败场景：图书不存在"""
        # 尝试归还不存在的图书
        result = self.book_service.return_book(999)
        
        # 验证结果
        assert result is False
    
    def test_return_book_already_available(self):
        """测试归还图书失败场景：图书已全部归还"""
        # 先添加一本图书
        added_book = self.book_service.add_book(**self.test_book_data)
        
        # 尝试归还未借阅的图书
        result = self.book_service.return_book(added_book.book_id)
        
        # 验证结果
        assert result is False
