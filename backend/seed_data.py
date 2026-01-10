from app import app, db
from models import User, Region, ServiceNeed, ServiceResponse, ResponseSuccess
from datetime import datetime, timedelta
import random

# 创建应用上下文
with app.app_context():
    print("正在清空旧数据...")
    # 1. 清空所有相关表 (注意外键约束，从子表删起)
    db.session.query(ResponseSuccess).delete()
    db.session.query(ServiceResponse).delete()
    db.session.query(ServiceNeed).delete()
    db.session.query(Region).delete()
    db.session.query(User).delete()
    db.session.commit()
    print("旧数据已清空！")

    print("正在初始化基础数据...")
    # 2. 插入地域
    regions_data = [
        Region(province='广东省', city='广州市', name='越秀区'),
        Region(province='广东省', city='广州市', name='海珠区'),
        Region(province='广东省', city='广州市', name='天河区'),
        Region(province='广东省', city='深圳市', name='福田区'),
        Region(province='广东省', city='深圳市', name='南山区'),
        Region(province='广东省', city='深圳市', name='罗湖区'),
        Region(province='浙江省', city='杭州市', name='西湖区'),
        Region(province='浙江省', city='杭州市', name='上城区'),
    ]
    db.session.add_all(regions_data)
    db.session.commit()
    regions = Region.query.all()

    # 3. 插入用户
    # 管理员
    admin = User(username='admin', password='admin', user_type='admin', real_name='系统管理员', phone='13800138000')
    db.session.add(admin)
    
    # 普通用户 (生成20个用户，让生态更丰富)
    users = []
    for i in range(1, 21):
        # 注意：这里 i 最大为20，phone 长度控制在11位
        phone_num = f"139000000{i:02d}" # 格式化为 01, 02... 保证长度
        user = User(
            username=f'user{i}', 
            password='Pass1234', 
            user_type='normal', 
            real_name=f'社区居民{i}', 
            phone=phone_num,
            bio=f'我是社区居民{i}，热心肠，喜欢帮助大家。'
        )
        users.append(user)
        db.session.add_all(users)
    
    db.session.commit()
    # 重新获取用户列表用于随机选择
    all_users = User.query.filter_by(user_type='normal').all()
    print(f"基础数据初始化完成：{len(regions)}个地域，{len(all_users)}个用户。")

    print("正在生成海量业务模拟数据 (2023.01 - 2023.06)...")
    
    service_types = ['管道维修', '助老服务', '保洁服务', '定期接送服务', '营养餐服务', '就诊服务']
    
    # 生成 2023年1月 到 6月 的数据
    months = ['202301', '202302', '202303', '202304', '202305', '202306']
    
    total_needs = 0
    total_success = 0

    for month_str in months:
        year = int(month_str[:4])
        month = int(month_str[4:])
        
        # 每个月随机生成 50 到 100 条需求
        monthly_count = random.randint(50, 100)
        print(f"  正在生成 {month_str} 数据: 计划 {monthly_count} 条...")
        
        for _ in range(monthly_count):
            # 1. 随机基础信息
            day = random.randint(1, 28) # 避开大小月问题，简单处理
            hour = random.randint(8, 22)
            create_time = datetime(year, month, day, hour, random.randint(0, 59))
            
            publisher = random.choice(all_users)
            region = random.choice(regions)
            stype = random.choice(service_types)
            
            # 2. 创建需求
            need = ServiceNeed(
                user_id=publisher.id,
                region_id=region.id,
                service_type=stype,
                subject=f"急需{region.city}{region.name}{stype}人员",
                description=f"我们在{region.name}遇到了一些问题，需要专业的{stype}人员帮忙，请尽快联系。",
                status=0, # 默认为0，后面根据逻辑修改
                created_at=create_time,
                updated_at=create_time
            )
            db.session.add(need)
            db.session.flush() # 拿到 need.id
            total_needs += 1

            # 3. 随机决定该需求的状态
            # 80% 概率会有响应
            if random.random() < 0.8:
                # 随机生成 1 到 3 个响应
                response_count = random.randint(1, 3)
                has_accepted = False # 标记是否已经有人被接受了

                for _ in range(response_count):
                    responder = random.choice([u for u in all_users if u.id != publisher.id])
                    resp_time = create_time + timedelta(minutes=random.randint(10, 300))
                    
                    resp = ServiceResponse(
                        need_id=need.id,
                        user_id=responder.id,
                        content=f"我可以提供{stype}，我有经验，就在附近。",
                        status=0,
                        created_at=resp_time,
                        updated_at=resp_time
                    )
                    db.session.add(resp)
                    db.session.flush()

                    # 逻辑：如果这个需求还没被解决，决定是否接受这个响应
                    # 60% 概率会成交 (ResponseSuccess)
                    if not has_accepted and random.random() < 0.6:
                        # 变成成交状态
                        need.status = 1  # 需求状态：已完成(1)
                        resp.status = 1  # 响应状态：已接受(1)
                        resp.updated_at = resp_time + timedelta(hours=1)
                        need.updated_at = resp_time + timedelta(hours=1)
                        
                        # 插入成功记录表
                        succ = ResponseSuccess(
                            need_id=need.id,
                            need_user_id=publisher.id,
                            response_id=resp.id,
                            response_user_id=responder.id,
                            accept_date=resp.updated_at,
                            created_at=resp.updated_at
                        )
                        db.session.add(succ)
                        has_accepted = True
                        total_success += 1
                    
                    # 如果已经有人被接受了，其他的响应大概率是拒绝(2)或者闲置(0)
                    elif has_accepted:
                        if random.random() < 0.8:
                            resp.status = 2 # 拒绝
            
            # 还有 10% 的概率需求被取消
            elif random.random() < 0.1:
                need.status = -1 # 已取消

    db.session.commit()
    print("="*50)
    print(f"数据生成完毕！")
    print(f"共生成需求: {total_needs} 条")
    print(f"共达成交易: {total_success} 单")
    print("请重启后端程序 (python app.py)，然后刷新前端页面查看漂亮的统计图！")