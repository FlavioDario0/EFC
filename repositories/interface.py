from abc import ABC, abstractmethod

class IOrderRepository(ABC):
    @abstractmethod
    def add(self, client, items_str, total, status, date, client_type): pass
    
    @abstractmethod
    def get(self, order_id): pass
    
    @abstractmethod
    def update_status(self, order_id, status): pass
    
    @abstractmethod
    def get_all_by_client(self, client): pass
    
    @abstractmethod
    def get_all(self): pass
    
    @abstractmethod
    def get_all_clients(self): pass
    
    @abstractmethod
    def close(self): pass

class INotificationService(ABC):
    @abstractmethod
    def notify_received(self, client, client_type): pass
    
    @abstractmethod
    def notify_approved(self, client, client_type): pass
    
    @abstractmethod
    def notify_shipped(self, client): pass
    
    @abstractmethod
    def notify_delivered(self, client, client_type, total): pass

class IStockService(ABC):
    @abstractmethod
    def validate(self, items): pass