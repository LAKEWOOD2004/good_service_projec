from app import app, db
from models import User, Region, ServiceNeed, ServiceResponse, ResponseSuccess, MonthlySummary
from datetime import datetime, timedelta

with app.app_context():
    # 清空旧数据
    db.session.query(ResponseSuccess).delete()
    db.session.query(ServiceResponse).delete()
    db.session.query(ServiceNeed).delete()
    db.session.query(MonthlySummary).delete()
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
        User(username='user4', password='Pass1234', user_type='normal', real_name='用户4', phone='13800138004', bio='助老服务志愿者'),
        User(username='user5', password='Pass1234', user_type='normal', real_name='用户5', phone='13800138005', bio='专业家政服务'),
    ]
    
    for user in test_users:
        db.session.add(user)
    
    # 插入测试服务需求
    service_types = ['管道维修', '助老服务', '保洁服务']
    regions = Region.query.all()
    users = User.query.filter(User.username != 'admin').all()
    
    service_needs = []
    for i in range(5):
        # 创建5个服务需求
        service_need = ServiceNeed(
            user_id=users[i % len(users)].id,
            region_id=regions[i % len(regions)].id,
            service_type=service_types[i % len(service_types)],
            subject=f'测试需求{i+1}',
            description=f'这是测试需求{i+1}的详细描述',
            status=0,  # 活跃状态
            created_at=datetime.now() - timedelta(days=i*7)
        )
        service_needs.append(service_need)
        db.session.add(service_need)
    
    # 插入测试服务响应
    service_responses = []
    for i, need in enumerate(service_needs):
        # 每个需求创建2个响应
        for j in range(2):
            service_response = ServiceResponse(
                need_id=need.id,
                user_id=users[(i+j+1) % len(users)].id,
                content=f'这是对需求{need.id}的第{j+1}个响应',
                status=0,  # 待接受
                created_at=datetime.now() - timedelta(days=i*7 + 1 + j)
            )
            service_responses.append(service_response)
            db.session.add(service_response)
    
    # 插入测试响应成功记录
    for i in range(0, len(service_responses), 2):
        # 每2个响应中标记1个为成功
        if i < len(service_needs):
            success = ResponseSuccess(
                need_id=service_needs[i].id,
                need_user_id=service_needs[i].user_id,
                response_id=service_responses[i].id,
                response_user_id=service_responses[i].user_id,
                accept_date=datetime.now() - timedelta(days=i*7 + 2)
            )
            db.session.add(success)
            # 更新响应状态为已接受
            service_responses[i].status = 1
    
    # 重新计算月度汇总数据
    # 获取所有需要统计的服务需求
    all_needs = ServiceNeed.query.all()
    all_successes = ResponseSuccess.query.all()
    
    # 按月份、地域、服务类型分组统计
    stats_map = {}
    
    # 统计服务需求数
    for need in all_needs:
        # 获取月份 (YYYYMM格式)
        month = need.created_at.strftime('%Y%m')
        
        # 获取地域信息
        region = Region.query.get(need.region_id)
        province = region.province if region else '未知'
        city = region.city if region else '未知'
        
        # 服务类型
        service_type = need.service_type
        
        # 生成唯一键
        key = f"{month}|{province}|{city}|{service_type}"
        
        # 初始化或更新统计数据
        if key not in stats_map:
            stats_map[key] = {
                'month': month,
                'province': province,
                'city': city,
                'service_type': service_type,
                'need_count': 0,
                'response_success_count': 0
            }
        
        stats_map[key]['need_count'] += 1
    
    # 统计响应成功数
    for success in all_successes:
        # 获取需求信息
        need = ServiceNeed.query.get(success.need_id)
        if not need:
            continue
        
        # 获取月份 (YYYYMM格式)
        month = success.accept_date.strftime('%Y%m')
        
        # 获取地域信息
        region = Region.query.get(need.region_id)
        province = region.province if region else '未知'
        city = region.city if region else '未知'
        
        # 服务类型
        service_type = need.service_type
        
        # 生成唯一键
        key = f"{month}|{province}|{city}|{service_type}"
        
        # 初始化或更新统计数据
        if key not in stats_map:
            stats_map[key] = {
                'month': month,
                'province': province,
                'city': city,
                'service_type': service_type,
                'need_count': 0,
                'response_success_count': 0
            }
        
        stats_map[key]['response_success_count'] += 1
    
    # 插入月度汇总数据
    for stat_data in stats_map.values():
        monthly_summary = MonthlySummary(**stat_data)
        db.session.add(monthly_summary)
    
    db.session.commit()
    print("数据初始化成功！")
