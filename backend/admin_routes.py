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
            # 按服务类型统计需求
            needs_by_type = db.session.query(
                ServiceNeed.service_type,
                func.count(ServiceNeed.id).label('need_count')
            ).filter(ServiceNeed.status == 0).group_by(
                ServiceNeed.service_type
            ).all()
            
            # 按服务类型统计成功响应
            success_by_type = db.session.query(
                ServiceNeed.service_type,
                func.count(ResponseSuccess.id).label('success_count')
            ).join(
                ResponseSuccess, ServiceNeed.id == ResponseSuccess.need_id
            ).group_by(
                ServiceNeed.service_type
            ).all()
            
            # 合并数据
            type_stats = {}
            for service_type, need_count in needs_by_type:
                type_stats[service_type] = {'need_count': need_count, 'success_count': 0}
            
            for service_type, success_count in success_by_type:
                if service_type in type_stats:
                    type_stats[service_type]['success_count'] = success_count
                else:
                    type_stats[service_type] = {'need_count': 0, 'success_count': success_count}
            
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
            # 按地域统计需求
            needs_by_region = db.session.query(
                (func.concat(Region.province, '-', Region.city, '-', Region.name)).label('region_name'),
                func.count(ServiceNeed.id).label('need_count')
            ).join(
                ServiceNeed, Region.id == ServiceNeed.region_id
            ).filter(ServiceNeed.status == 0).group_by(
                Region.id, Region.province, Region.city, Region.name
            ).all()
            
            # 按地域统计成功响应
            success_by_region = db.session.query(
                (func.concat(Region.province, '-', Region.city, '-', Region.name)).label('region_name'),
                func.count(ResponseSuccess.id).label('success_count')
            ).join(
                ServiceNeed, Region.id == ServiceNeed.region_id
            ).join(
                ResponseSuccess, ServiceNeed.id == ResponseSuccess.need_id
            ).group_by(
                Region.id, Region.province, Region.city, Region.name
            ).all()
            
            # 合并数据
            region_stats = {}
            for region_name, need_count in needs_by_region:
                region_stats[region_name] = {'need_count': need_count, 'success_count': 0}
            
            for region_name, success_count in success_by_region:
                if region_name in region_stats:
                    region_stats[region_name]['success_count'] = success_count
                else:
                    region_stats[region_name] = {'need_count': 0, 'success_count': success_count}
            
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
            
            # 构建查询条件
            query = MonthlySummary.query
            
            # 按时间段筛选
            if start_month:
                query = query.filter(MonthlySummary.month >= start_month)
            if end_month:
                query = query.filter(MonthlySummary.month <= end_month)
            
            # 按地域筛选
            if province:
                query = query.filter(MonthlySummary.province == province)
            if city:
                query = query.filter(MonthlySummary.city == city)
            
            # 按服务类型筛选
            if service_type:
                query = query.filter(MonthlySummary.service_type.contains(service_type))
            
            # 排序
            if sort_by in ['need_count', 'response_success_count']:
                if sort_order == 'asc':
                    query = query.order_by(getattr(MonthlySummary, sort_by).asc())
                else:
                    query = query.order_by(getattr(MonthlySummary, sort_by).desc())
            else:
                # 默认按月份降序
                query = query.order_by(MonthlySummary.month.desc())
            
            # 分页
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)
            
            # 构建响应数据
            items = []
            for summary in pagination.items:
                items.append({
                    'id': summary.id,
                    'month': summary.month,
                    'province': summary.province,
                    'city': summary.city,
                    'region': f"{summary.province}-{summary.city}",
                    'service_type': summary.service_type,
                    'need_count': summary.need_count,
                    'response_success_count': summary.response_success_count,
                    'created_at': summary.created_at.strftime('%Y-%m-%d %H:%M:%S') if summary.created_at else '',
                    'updated_at': summary.updated_at.strftime('%Y-%m-%d %H:%M:%S') if summary.updated_at else ''
                })
            
            return jsonify({
                "code": 200,
                "data": items,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": pagination.total,
                    "pages": pagination.pages
                }
            }), 200
        except Exception as e:
            return jsonify({"code": 500, "msg": f"系统错误: {str(e)}"}), 500
