from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# 1. 用户信息类
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(20), default='normal') # admin or normal
    real_name = db.Column(db.String(50))
    phone = db.Column(db.String(11))
    bio = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

# 2. 地域信息表
class Region(db.Model):
    __tablename__ = 'regions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False) # 区县
    city = db.Column(db.String(50), nullable=False) # 地市
    province = db.Column(db.String(50), nullable=False) # 省份

# 3. "我需要"需求信息类
class ServiceNeed(db.Model):
    __tablename__ = 'service_needs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # 发布者
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id')) # 地域
    service_type = db.Column(db.String(50), nullable=False) # 管道维修、保洁等
    subject = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    media_url = db.Column(db.String(255)) # 图片或视频路径
    status = db.Column(db.Integer, default=0) # 0:已发布; -1:已取消
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

# 4. "我服务"响应信息类
class ServiceResponse(db.Model):
    __tablename__ = 'service_responses'
    id = db.Column(db.Integer, primary_key=True)
    need_id = db.Column(db.Integer, db.ForeignKey('service_needs.id'), nullable=False) # 关联的需求
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # 响应者
    content = db.Column(db.Text, nullable=False)
    media_url = db.Column(db.String(255)) # 响应介绍图片或视频
    status = db.Column(db.Integer, default=0) # 0:待接受; 1:同意; 2:拒绝; 3:取消
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

# 5. "好服务"响应成功明细类
class ResponseSuccess(db.Model):
    __tablename__ = 'response_success'
    id = db.Column(db.Integer, primary_key=True)
    need_id = db.Column(db.Integer, db.ForeignKey('service_needs.id'), nullable=False) # 需求标识
    need_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # 发布需求用户
    response_id = db.Column(db.Integer, db.ForeignKey('service_responses.id'), nullable=False) # 响应标识
    response_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # 响应用户
    accept_date = db.Column(db.DateTime, default=datetime.now)
    created_at = db.Column(db.DateTime, default=datetime.now)

# 6. 响应成功月汇总信息类
class MonthlySummary(db.Model):
    __tablename__ = 'monthly_summary'
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.String(6), nullable=False) # YYYYMM格式
    province = db.Column(db.String(50))
    city = db.Column(db.String(50))
    service_type = db.Column(db.String(50))
    need_count = db.Column(db.Integer, default=0) # 月累计发布服务需求数
    response_success_count = db.Column(db.Integer, default=0) # 月累计响应成功服务数
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

# 导入事件监听器需要的模块
from sqlalchemy import event

# 定义更新月度统计的辅助函数
def update_single_monthly_summary(record, is_need=True):
    """
    更新单条记录对应的月度统计
    
    参数:
        record: 新增或修改的记录对象 (ServiceNeed或ResponseSuccess)
        is_need: 是否为服务需求记录
    """
    from app import app
    with app.app_context():
        if is_need:
            # 处理ServiceNeed记录
            need = record
            month = need.created_at.strftime('%Y%m')
            region = Region.query.get(need.region_id)
            province = region.province if region else '未知'
            city = region.city if region else '未知'
            service_type = need.service_type
            
            # 生成唯一键
            key = f"{month}|{province}|{city}|{service_type}"
            
            # 查找或创建月度统计记录
            existing = MonthlySummary.query.filter(
                MonthlySummary.month == month,
                MonthlySummary.province == province,
                MonthlySummary.city == city,
                MonthlySummary.service_type == service_type
            ).first()
            
            if existing:
                existing.need_count += 1
            else:
                new_summary = MonthlySummary(
                    month=month,
                    province=province,
                    city=city,
                    service_type=service_type,
                    need_count=1,
                    response_success_count=0
                )
                db.session.add(new_summary)
        else:
            # 处理ResponseSuccess记录
            success = record
            need = ServiceNeed.query.get(success.need_id)
            if need:
                month = success.accept_date.strftime('%Y%m')
                region = Region.query.get(need.region_id)
                province = region.province if region else '未知'
                city = region.city if region else '未知'
                service_type = need.service_type
                
                # 生成唯一键
                key = f"{month}|{province}|{city}|{service_type}"
                
                # 查找或创建月度统计记录
                existing = MonthlySummary.query.filter(
                    MonthlySummary.month == month,
                    MonthlySummary.province == province,
                    MonthlySummary.city == city,
                    MonthlySummary.service_type == service_type
                ).first()
                
                if existing:
                    existing.response_success_count += 1
                else:
                    new_summary = MonthlySummary(
                        month=month,
                        province=province,
                        city=city,
                        service_type=service_type,
                        need_count=0,
                        response_success_count=1
                    )
                    db.session.add(new_summary)
        
        db.session.commit()

# 为ServiceNeed添加事件监听器，在插入数据后更新月度统计
@event.listens_for(ServiceNeed, 'after_insert')
def after_service_need_insert(mapper, connection, target):
    update_single_monthly_summary(target, is_need=True)

# 为ResponseSuccess添加事件监听器，在插入数据后更新月度统计
@event.listens_for(ResponseSuccess, 'after_insert')
def after_response_success_insert(mapper, connection, target):
    update_single_monthly_summary(target, is_need=False)