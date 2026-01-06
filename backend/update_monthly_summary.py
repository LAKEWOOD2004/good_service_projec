from app import app, db
from models import ServiceNeed, ServiceResponse, ResponseSuccess, MonthlySummary, Region
from datetime import datetime


def update_monthly_summary(start_date=None, end_date=None):
    """
    更新月度统计数据
    根据ServiceNeed和ResponseSuccess表中的实际数据计算月度汇总统计
    
    参数:
        start_date: 起始日期 (datetime对象，可选)
        end_date: 终止日期 (datetime对象，可选)
    """
    with app.app_context():
        # 获取需要统计的所有ServiceNeed
        need_query = ServiceNeed.query
        if start_date:
            need_query = need_query.filter(ServiceNeed.created_at >= start_date)
        if end_date:
            need_query = need_query.filter(ServiceNeed.created_at <= end_date)
        
        all_needs = need_query.all()
        
        # 获取需要统计的所有ResponseSuccess
        success_query = ResponseSuccess.query
        if start_date:
            success_query = success_query.filter(ResponseSuccess.accept_date >= start_date)
        if end_date:
            success_query = success_query.filter(ResponseSuccess.accept_date <= end_date)
        
        all_successes = success_query.all()
        
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
        
        # 更新数据库
        for stat_key, stat_data in stats_map.items():
            # 查找现有记录
            existing = MonthlySummary.query.filter(
                MonthlySummary.month == stat_data['month'],
                MonthlySummary.province == stat_data['province'],
                MonthlySummary.city == stat_data['city'],
                MonthlySummary.service_type == stat_data['service_type']
            ).first()
            
            if existing:
                # 更新现有记录
                existing.need_count = stat_data['need_count']
                existing.response_success_count = stat_data['response_success_count']
                existing.updated_at = datetime.now()
            else:
                # 创建新记录
                new_summary = MonthlySummary(**stat_data)
                db.session.add(new_summary)
        
        db.session.commit()
        print(f"月度统计数据更新成功，共处理 {len(stats_map)} 条记录")
        
        return len(stats_map)


if __name__ == "__main__":
    # 执行更新
    update_monthly_summary()
