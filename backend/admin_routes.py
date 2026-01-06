"""
管理员统计模块 - 用于显示系统的各种统计数据
包括地域统计、服务类型统计、用户活跃度等
"""

from flask import request, jsonify
from datetime import datetime
from models import db, ServiceNeed, ServiceResponse, ResponseSuccess, User, Region, MonthlySummary
from sqlalchemy import func, and_


def register_admin_routes(app):
    """注册所有管理员统计相关的API路由"""
    
    @app.route('/api/admin/stats/overview', methods=['GET'])
    def get_overview_stats():
        """获取系统概览统计"""
        try:
            # 统计总数
            total_users = User.query.count()
            total_needs = ServiceNeed.query.filter_by(status=0).count()
            total_responses = ServiceResponse.query.count()
            total_success = ResponseSuccess.query.count()
            
            return jsonify({
                "code": 200,
                "data": {
                    "total_users": total_users,
                    "total_needs": total_needs,
                    "total_responses": total_responses,
                    "total_success": total_success
                }
            }), 200
        except Exception as e:
            return jsonify({"code": 500, "msg": f"系统错误: {str(e)}"}), 500
    
    
    @app.route('/api/admin/stats/by-service-type', methods=['GET'])
    def get_stats_by_service_type():
        """按服务类型统计需求和响应"""
        try:
            # 获取所有需要统计的服务需求
            need_query = ServiceNeed.query.filter(ServiceNeed.status == 0)  # 只统计活跃需求
            all_needs = need_query.all()
            
            # 获取所有需要统计的响应成功
            success_query = ResponseSuccess.query
            all_successes = success_query.all()
            
            # 按服务类型分组统计
            type_stats = {}
            
            # 统计服务需求数
            for need in all_needs:
                service_type = need.service_type
                
                # 初始化或更新统计数据
                if service_type not in type_stats:
                    type_stats[service_type] = {'need_count': 0, 'success_count': 0}
                
                type_stats[service_type]['need_count'] += 1
            
            # 统计响应成功数
            for success in all_successes:
                # 获取需求信息
                need = ServiceNeed.query.get(success.need_id)
                if not need:
                    continue
                
                service_type = need.service_type
                
                # 初始化或更新统计数据
                if service_type not in type_stats:
                    type_stats[service_type] = {'need_count': 0, 'success_count': 0}
                
                type_stats[service_type]['success_count'] += 1
            
            return jsonify({
                "code": 200,
                "data": type_stats
            }), 200
        except Exception as e:
            return jsonify({"code": 500, "msg": f"系统错误: {str(e)}"}), 500
    
    
    @app.route('/api/admin/stats/by-region', methods=['GET'])
    def get_stats_by_region():
        """按地域统计需求和响应"""
        try:
            # 获取所有需要统计的服务需求
            need_query = ServiceNeed.query.filter(ServiceNeed.status == 0)  # 只统计活跃需求
            all_needs = need_query.all()
            
            # 获取所有需要统计的响应成功
            success_query = ResponseSuccess.query
            all_successes = success_query.all()
            
            # 按地域分组统计
            region_stats = {}
            
            # 统计服务需求数
            for need in all_needs:
                # 获取地域信息
                region = Region.query.get(need.region_id)
                region_name = f"{region.province}-{region.city}-{region.name}" if region else '未知地域'
                
                # 初始化或更新统计数据
                if region_name not in region_stats:
                    region_stats[region_name] = {'need_count': 0, 'success_count': 0}
                
                region_stats[region_name]['need_count'] += 1
            
            # 统计响应成功数
            for success in all_successes:
                # 获取需求信息
                need = ServiceNeed.query.get(success.need_id)
                if not need:
                    continue
                
                # 获取地域信息
                region = Region.query.get(need.region_id)
                region_name = f"{region.province}-{region.city}-{region.name}" if region else '未知地域'
                
                # 初始化或更新统计数据
                if region_name not in region_stats:
                    region_stats[region_name] = {'need_count': 0, 'success_count': 0}
                
                region_stats[region_name]['success_count'] += 1
            
            return jsonify({
                "code": 200,
                "data": region_stats
            }), 200
        except Exception as e:
            return jsonify({"code": 500, "msg": f"系统错误: {str(e)}"}), 500
    
    
    @app.route('/api/admin/stats/response-rate', methods=['GET'])
    def get_response_rate_stats():
        """获取响应成功率统计"""
        try:
            # 总需求数
            total_needs = ServiceNeed.query.filter_by(status=0).count()
            
            # 有响应的需求数
            needs_with_response = db.session.query(
                func.count(func.distinct(ServiceResponse.need_id))
            ).filter(ServiceResponse.status != 3).scalar() or 0
            
            # 被接受的需求数(有成功配对)
            needs_with_success = db.session.query(
                func.count(func.distinct(ResponseSuccess.need_id))
            ).scalar() or 0
            
            # 计算成功率
            response_rate = (needs_with_response / total_needs * 100) if total_needs > 0 else 0
            success_rate = (needs_with_success / total_needs * 100) if total_needs > 0 else 0
            
            return jsonify({
                "code": 200,
                "data": {
                    "total_needs": total_needs,
                    "needs_with_response": needs_with_response,
                    "needs_with_success": needs_with_success,
                    "response_rate": round(response_rate, 2),
                    "success_rate": round(success_rate, 2)
                }
            }), 200
        except Exception as e:
            return jsonify({"code": 500, "msg": f"系统错误: {str(e)}"}), 500
    
    
    @app.route('/api/admin/stats/user-activity', methods=['GET'])
    def get_user_activity_stats():
        """获取用户活跃度统计"""
        try:
            # 发布需求最多的前5个用户
            top_need_publishers = db.session.query(
                User.real_name,
                func.count(ServiceNeed.id).label('need_count')
            ).join(
                ServiceNeed, User.id == ServiceNeed.user_id
            ).group_by(User.id, User.real_name).order_by(
                func.count(ServiceNeed.id).desc()
            ).limit(5).all()
            
            # 提供响应最多的前5个用户
            top_responders = db.session.query(
                User.real_name,
                func.count(ServiceResponse.id).label('response_count')
            ).join(
                ServiceResponse, User.id == ServiceResponse.user_id
            ).group_by(User.id, User.real_name).order_by(
                func.count(ServiceResponse.id).desc()
            ).limit(5).all()
            
            return jsonify({
                "code": 200,
                "data": {
                    "top_need_publishers": [
                        {"name": name, "count": count} 
                        for name, count in top_need_publishers
                    ],
                    "top_responders": [
                        {"name": name, "count": count} 
                        for name, count in top_responders
                    ]
                }
            }), 200
        except Exception as e:
            return jsonify({"code": 500, "msg": f"系统错误: {str(e)}"}), 500
    
    
    @app.route('/api/admin/stats/monthly-summary', methods=['GET'])
    def get_monthly_summary_stats():
        """
        获取月度汇总统计数据
        支持按时间段、地域条件查询，返回明细列表
        直接从实际业务表计算，确保数据一致性
        
        参数:
            start_month: 起始年月 (YYYYMM格式，如202301)
            end_month: 终止年月 (YYYYMM格式，如202303)
            province: 省份 (可选)
            city: 城市 (可选)
            service_type: 服务类型 (可选)
            sort_by: 排序字段 (可选，如need_count或response_success_count)
            sort_order: 排序方向 (可选，asc或desc，默认desc)
            page: 页码 (默认1)
            per_page: 每页条数 (默认10)
        """
        try:
            # 获取查询参数
            start_month = request.args.get('start_month', type=str)
            end_month = request.args.get('end_month', type=str)
            province = request.args.get('province', type=str)
            city = request.args.get('city', type=str)
            service_type = request.args.get('service_type', type=str)
            sort_by = request.args.get('sort_by', default='need_count', type=str)
            sort_order = request.args.get('sort_order', default='desc', type=str)
            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=10, type=int)
            
            # 获取所有需要统计的服务需求
            need_query = ServiceNeed.query.filter(ServiceNeed.status == 0)  # 只统计活跃需求
            all_needs = need_query.all()
            
            # 获取所有需要统计的响应成功
            success_query = ResponseSuccess.query
            all_successes = success_query.all()
            
            # 按月份、地域、服务类型分组统计
            stats_map = {}
            
            # 统计服务需求数
            for need in all_needs:
                # 获取月份 (YYYYMM格式)
                month = need.created_at.strftime('%Y%m')
                
                # 跳过不在查询范围内的月份
                if start_month and month < start_month:
                    continue
                if end_month and month > end_month:
                    continue
                
                # 获取地域信息
                region = Region.query.get(need.region_id)
                need_province = region.province if region else '未知'
                need_city = region.city if region else '未知'
                
                # 处理城市筛选条件（前端传递的格式：省份-城市，如"广东省-广州市"）
                city_to_compare = f"{need_province}-{need_city}" if region else '未知-未知'
                
                # 跳过不在查询范围内的地域
                if province and need_province != province:
                    continue
                if city and city not in city_to_compare:
                    continue
                
                # 跳过不在查询范围内的服务类型
                if service_type and service_type != need.service_type:
                    continue
                
                # 服务类型
                need_service_type = need.service_type
                
                # 生成唯一键
                key = f"{month}|{need_province}|{need_city}|{need_service_type}"
                
                # 初始化或更新统计数据
                if key not in stats_map:
                    stats_map[key] = {
                        'month': month,
                        'province': need_province,
                        'city': need_city,
                        'service_type': need_service_type,
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
                
                # 跳过不在查询范围内的月份
                if start_month and month < start_month:
                    continue
                if end_month and month > end_month:
                    continue
                
                # 获取地域信息
                region = Region.query.get(need.region_id)
                success_province = region.province if region else '未知'
                success_city = region.city if region else '未知'
                
                # 处理城市筛选条件（前端传递的格式：省份-城市，如"广东省-广州市"）
                city_to_compare = f"{success_province}-{success_city}" if region else '未知-未知'
                
                # 跳过不在查询范围内的地域
                if province and success_province != province:
                    continue
                if city and city not in city_to_compare:
                    continue
                
                # 跳过不在查询范围内的服务类型
                if service_type and service_type != need.service_type:
                    continue
                
                # 服务类型
                success_service_type = need.service_type
                
                # 生成唯一键
                key = f"{month}|{success_province}|{success_city}|{success_service_type}"
                
                # 初始化或更新统计数据
                if key not in stats_map:
                    stats_map[key] = {
                        'month': month,
                        'province': success_province,
                        'city': success_city,
                        'service_type': success_service_type,
                        'need_count': 0,
                        'response_success_count': 0
                    }
                
                stats_map[key]['response_success_count'] += 1
            
            # 如果没有数据，返回空列表
            if len(stats_map) == 0:
                return jsonify({
                    "code": 200,
                    "data": [],
                    "pagination": {
                        "page": 1,
                        "per_page": per_page,
                        "total": 0,
                        "pages": 0
                    }
                }), 200
            
            # 转换为列表并排序
            stats_list = list(stats_map.values())
            
            # 排序
            stats_list.sort(key=lambda x: (
                # 先按月份排序（降序）
                -int(x['month']),
                # 再按指定字段排序
                x[sort_by] if sort_order == 'asc' else -x[sort_by]
            ))
            
            # 手动分页
            total = len(stats_list)
            pages = (total + per_page - 1) // per_page
            start = (page - 1) * per_page
            end = start + per_page
            paginated_stats = stats_list[start:end]
            
            # 构建响应数据
            items = []
            for index, stat in enumerate(paginated_stats, 1):
                items.append({
                    'id': index,
                    'month': stat['month'],
                    'province': stat['province'],
                    'city': stat['city'],
                    'region': f"{stat['province']}-{stat['city']}",
                    'service_type': stat['service_type'],
                    'need_count': stat['need_count'],
                    'response_success_count': stat['response_success_count'],
                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
            
            return jsonify({
                "code": 200,
                "data": items,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": total,
                    "pages": pages
                }
            }), 200
            
        except Exception as e:
            return jsonify({"code": 500, "msg": f"系统错误: {str(e)}"}), 500
    
    
    @app.route('/api/admin/stats/update-monthly-summary', methods=['POST'])
    def update_monthly_summary_stats():
        """
        手动更新月度统计数据
        支持按时间段更新
        
        参数:
            start_date: 起始日期 (YYYY-MM-DD格式，可选)
            end_date: 终止日期 (YYYY-MM-DD格式，可选)
        """
        try:
            # 导入更新函数
            from update_monthly_summary import update_monthly_summary
            from datetime import datetime
            
            # 获取请求参数
            start_date_str = request.json.get('start_date')
            end_date_str = request.json.get('end_date')
            
            # 解析日期
            start_date = None
            end_date = None
            
            if start_date_str:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            
            if end_date_str:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            
            # 执行更新
            updated_count = update_monthly_summary(start_date, end_date)
            
            return jsonify({
                "code": 200,
                "msg": f"月度统计数据更新成功，共处理 {updated_count} 条记录",
                "data": {
                    "updated_count": updated_count
                }
            }), 200
        except Exception as e:
            return jsonify({"code": 500, "msg": f"系统错误: {str(e)}"}), 500
