from app import app, db
from models import User, Region, MonthlySummary

with app.app_context():
    # 清空旧数据
    db.session.query(Region).delete()
    db.session.query(User).delete()
    
    # 插入地域信息
    regions = [
        Region(province='广东省', city='广州市', name='越秀区'),
        Region(province='广东省', city='广州市', name='海珠区'),
        Region(province='广东省', city='广州市', name='荔湾区'),
        Region(province='广东省', city='深圳市', name='福田区'),
        Region(province='广东省', city='深圳市', name='南山区'),
        Region(province='江苏省', city='南京市', name='玄武区'),
        Region(province='江苏省', city='南京市', name='秦淮区'),
        Region(province='浙江省', city='杭州市', name='西湖区'),
        Region(province='浙江省', city='杭州市', name='上城区'),
    ]
    
    for region in regions:
        db.session.add(region)
    
    # 插入管理员用户
    admin = User(
        username='admin',
        password='admin',
        user_type='admin',
        real_name='系统管理员',
        phone='13800138000'
    )
    db.session.add(admin)
    
    # 插入测试用户
    test_users = [
        User(username='user1', password='Pass1234', user_type='normal', real_name='用户1', phone='13800138001', bio='我喜欢帮助他人'),
        User(username='user2', password='Pass1234', user_type='normal', real_name='用户2', phone='13800138002', bio='专业管道维修'),
        User(username='user3', password='Pass1234', user_type='normal', real_name='用户3', phone='13800138003', bio='保洁服务专业人士'),
    ]
    
    for user in test_users:
        db.session.add(user)
    
    # 清空旧的月度汇总数据
    db.session.query(MonthlySummary).delete()
    
    # 插入月度汇总测试数据
    monthly_data = [
        # 广东省-广州市 数据
        MonthlySummary(month='202301', province='广东省', city='广州市', service_type='管道维修', need_count=12, response_success_count=8),
        MonthlySummary(month='202301', province='广东省', city='广州市', service_type='助老服务', need_count=25, response_success_count=20),
        MonthlySummary(month='202301', province='广东省', city='广州市', service_type='保洁服务', need_count=18, response_success_count=15),
        MonthlySummary(month='202302', province='广东省', city='广州市', service_type='管道维修', need_count=15, response_success_count=12),
        MonthlySummary(month='202302', province='广东省', city='广州市', service_type='助老服务', need_count=28, response_success_count=22),
        MonthlySummary(month='202302', province='广东省', city='广州市', service_type='保洁服务', need_count=20, response_success_count=16),
        MonthlySummary(month='202303', province='广东省', city='广州市', service_type='管道维修', need_count=10, response_success_count=8),
        MonthlySummary(month='202303', province='广东省', city='广州市', service_type='助老服务', need_count=30, response_success_count=25),
        MonthlySummary(month='202303', province='广东省', city='广州市', service_type='保洁服务', need_count=22, response_success_count=18),
        # 广东省-深圳市 数据
        MonthlySummary(month='202301', province='广东省', city='深圳市', service_type='管道维修', need_count=8, response_success_count=6),
        MonthlySummary(month='202301', province='广东省', city='深圳市', service_type='助老服务', need_count=15, response_success_count=12),
        MonthlySummary(month='202301', province='广东省', city='深圳市', service_type='保洁服务', need_count=25, response_success_count=22),
        MonthlySummary(month='202302', province='广东省', city='深圳市', service_type='管道维修', need_count=10, response_success_count=7),
        MonthlySummary(month='202302', province='广东省', city='深圳市', service_type='助老服务', need_count=18, response_success_count=15),
        MonthlySummary(month='202302', province='广东省', city='深圳市', service_type='保洁服务', need_count=28, response_success_count=25),
        MonthlySummary(month='202303', province='广东省', city='深圳市', service_type='管道维修', need_count=12, response_success_count=9),
        MonthlySummary(month='202303', province='广东省', city='深圳市', service_type='助老服务', need_count=20, response_success_count=17),
        MonthlySummary(month='202303', province='广东省', city='深圳市', service_type='保洁服务', need_count=30, response_success_count=27),
        # 浙江省-杭州市 数据
        MonthlySummary(month='202301', province='浙江省', city='杭州市', service_type='管道维修', need_count=10, response_success_count=7),
        MonthlySummary(month='202301', province='浙江省', city='杭州市', service_type='助老服务', need_count=20, response_success_count=16),
        MonthlySummary(month='202301', province='浙江省', city='杭州市', service_type='保洁服务', need_count=15, response_success_count=12),
        MonthlySummary(month='202302', province='浙江省', city='杭州市', service_type='管道维修', need_count=12, response_success_count=9),
        MonthlySummary(month='202302', province='浙江省', city='杭州市', service_type='助老服务', need_count=22, response_success_count=18),
        MonthlySummary(month='202302', province='浙江省', city='杭州市', service_type='保洁服务', need_count=18, response_success_count=15),
        MonthlySummary(month='202303', province='浙江省', city='杭州市', service_type='管道维修', need_count=9, response_success_count=6),
        MonthlySummary(month='202303', province='浙江省', city='杭州市', service_type='助老服务', need_count=18, response_success_count=14),
        MonthlySummary(month='202303', province='浙江省', city='杭州市', service_type='保洁服务', need_count=20, response_success_count=17),
    ]
    
    for data in monthly_data:
        db.session.add(data)
    
    db.session.commit()
    print("数据初始化成功！")
