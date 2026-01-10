"""
管理员统计模块 - 实时计算版
直接从业务表中聚合数据，确保图表实时反映最新状态
"""

from flask import request, jsonify
from models import db, ServiceNeed, ServiceResponse, ResponseSuccess, User, Region
from sqlalchemy import func
from datetime import datetime
from collections import defaultdict

def register_admin_routes(app):
    """注册所有管理员统计相关的API路由"""
    
    @app.route('/api/admin/stats/overview', methods=['GET'])
    def get_overview_stats():
        """获取系统概览统计"""
        try:
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
        """按服务类型统计"""
        try:
            # 统计需求
            needs_by_type = db.session.query(
                ServiceNeed.service_type,
                func.count(ServiceNeed.id)
            ).filter(ServiceNeed.status == 0).group_by(ServiceNeed.service_type).all()
            
            # 统计成功响应
            success_by_type = db.session.query(
                ServiceNeed.service_type,
                func.count(ResponseSuccess.id)
            ).join(
                ResponseSuccess, ServiceNeed.id == ResponseSuccess.need_id
            ).group_by(ServiceNeed.service_type).all()
            
            type_stats = {}
            for stype, count in needs_by_type:
                type_stats[stype] = {'need_count': count, 'success_count': 0}
            
            for stype, count in success_by_type:
                if stype in type_stats:
                    type_stats[stype]['success_count'] = count
                else:
                    type_stats[stype] = {'need_count': 0, 'success_count': count}
            
            return jsonify({"code": 200, "data": type_stats}), 200
        except Exception as e:
            return jsonify({"code": 500, "msg": f"系统错误: {str(e)}"}), 500
    
    
    @app.route('/api/admin/stats/by-region', methods=['GET'])
    def get_stats_by_region():
        """按地域统计"""
        try:
            # 统计需求
            needs_by_region = db.session.query(
                (func.concat(Region.province, '-', Region.city, '-', Region.name)).label('region_name'),
                func.count(ServiceNeed.id)
            ).join(ServiceNeed, Region.id == ServiceNeed.region_id)\
             .filter(ServiceNeed.status == 0)\
             .group_by(Region.id, Region.province, Region.city, Region.name).all()
            
            # 统计成功
            success_by_region = db.session.query(
                (func.concat(Region.province, '-', Region.city, '-', Region.name)).label('region_name'),
                func.count(ResponseSuccess.id)
            ).join(ServiceNeed, Region.id == ServiceNeed.region_id)\
             .join(ResponseSuccess, ServiceNeed.id == ResponseSuccess.need_id)\
             .group_by(Region.id, Region.province, Region.city, Region.name).all()
            
            region_stats = {}
            for rname, count in needs_by_region:
                region_stats[rname] = {'need_count': count, 'success_count': 0}
            
            for rname, count in success_by_region:
                if rname in region_stats:
                    region_stats[rname]['success_count'] = count
                else:
                    region_stats[rname] = {'need_count': 0, 'success_count': count}
            
            return jsonify({"code": 200, "data": region_stats}), 200
        except Exception as e:
            return jsonify({"code": 500, "msg": f"系统错误: {str(e)}"}), 500
    
    
    @app.route('/api/admin/stats/response-rate', methods=['GET'])
    def get_response_rate_stats():
        """响应成功率"""
        try:
            total_needs = ServiceNeed.query.filter_by(status=0).count()
            
            needs_with_response = db.session.query(
                func.count(func.distinct(ServiceResponse.need_id))
            ).filter(ServiceResponse.status != 3).scalar() or 0
            
            needs_with_success = db.session.query(
                func.count(func.distinct(ResponseSuccess.need_id))
            ).scalar() or 0
            
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
        """用户活跃度"""
        try:
            top_publishers = db.session.query(User.real_name, func.count(ServiceNeed.id))\
                .join(ServiceNeed, User.id == ServiceNeed.user_id)\
                .group_by(User.id, User.real_name)\
                .order_by(func.count(ServiceNeed.id).desc()).limit(5).all()
            
            top_responders = db.session.query(User.real_name, func.count(ServiceResponse.id))\
                .join(ServiceResponse, User.id == ServiceResponse.user_id)\
                .group_by(User.id, User.real_name)\
                .order_by(func.count(ServiceResponse.id).desc()).limit(5).all()
            
            return jsonify({
                "code": 200,
                "data": {
                    "top_need_publishers": [{"name": n, "count": c} for n, c in top_publishers],
                    "top_responders": [{"name": n, "count": c} for n, c in top_responders]
                }
            }), 200
        except Exception as e:
            return jsonify({"code": 500, "msg": f"系统错误: {str(e)}"}), 500


    # 修改:实时聚合月度数据，不依赖 MonthlySummary 表
    @app.route('/api/admin/stats/monthly-summary', methods=['GET'])
    def get_monthly_summary_stats():
        """
        实时计算月度汇总数据
        """
        try:
            # 1. 获取所有需求和成功记录
            all_needs = ServiceNeed.query.all()
            all_successes = ResponseSuccess.query.all()
            
            # 2. 内存聚合
            summary_map = defaultdict(lambda: {'need_count': 0, 'success_count': 0})
            
            # ... (这部分统计逻辑不变，保持原样) ...
            for need in all_needs:
                if not need.created_at: continue
                month = need.created_at.strftime('%Y%m')
                key = (month, need.region_id, need.service_type)
                summary_map[key]['need_count'] += 1
                
            need_lookup = {n.id: n for n in all_needs}
            for success in all_successes:
                if not success.created_at: continue
                month = success.created_at.strftime('%Y%m')
                related_need = need_lookup.get(success.need_id)
                if related_need:
                    key = (month, related_need.region_id, related_need.service_type)
                    summary_map[key]['success_count'] += 1

            # 3. 过滤并生成列表
            data_list = []
            all_regions = {r.id: r for r in Region.query.all()}
            
            req_start = request.args.get('start_month')
            req_end = request.args.get('end_month')
            req_prov = request.args.get('province')
            req_city = request.args.get('city')
            req_type = request.args.get('service_type')
            
            for (month, region_id, service_type), stats in summary_map.items():
                region_obj = all_regions.get(region_id)
                
                if req_start and month < req_start: continue
                if req_end and month > req_end: continue
                if req_prov and region_obj and region_obj.province != req_prov: continue
                if req_city and region_obj and region_obj.city != req_city: continue
                if req_type and req_type not in service_type: continue
                
                data_list.append({
                    'id': f"{month}-{region_id}-{service_type}",
                    'month': month,
                    'province': region_obj.province if region_obj else '未知',
                    'city': region_obj.city if region_obj else '未知',
                    'region': f"{region_obj.province}-{region_obj.city}" if region_obj else '未知',
                    'service_type': service_type,
                    'need_count': stats['need_count'],
                    'response_success_count': stats['success_count']
                })

            # === 【新增代码开始】专门为图表生成聚合数据（不受分页影响） ===
            chart_agg = defaultdict(lambda: {'need': 0, 'success': 0})
            for item in data_list:
                m = item['month']
                chart_agg[m]['need'] += item['need_count']
                chart_agg[m]['success'] += item['response_success_count']
            
            # 转为列表并按月份升序 (图表必须时间正序)
            chart_data = []
            for m in sorted(chart_agg.keys()):
                chart_data.append({
                    'month': m,
                    'need_count': chart_agg[m]['need'],
                    'success_count': chart_agg[m]['success']
                })
            # === 【新增代码结束】 ===

            # 4. 列表排序 (表格默认倒序)
            data_list.sort(key=lambda x: x['month'], reverse=True)
            
            # 5. 分页处理 (只影响表格)
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            total = len(data_list)
            start = (page - 1) * per_page
            end = start + per_page
            paginated_items = data_list[start:end]
            
            return jsonify({
                "code": 200,
                "data": paginated_items,     # 给表格用的（分页）
                "chart_data": chart_data,    # 给图表用的（全量聚合）
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": total,
                    "pages": (total + per_page - 1) // per_page
                }
            }), 200
            
        except Exception as e:
            return jsonify({"code": 500, "msg": f"系统错误: {str(e)}"}), 500