"""
我要服务 - 服务响应/服务提供相关的API路由
用户通过这些API来对他人发布的服务需求进行响应，即提供服务帮助
"""

from flask import request, jsonify
from datetime import datetime
from models import db, ServiceResponse, ServiceNeed, User, Region


def register_service_response_routes(app):
    """注册所有服务响应相关的API路由"""
    
    @app.route('/api/service-responses', methods=['GET'])
    def list_service_responses():
        """
        获取所有服务响应列表 (所有用户发布的服务)
        支持分页、按需求类型筛选、按状态筛选
        
        参数:
            page: 页码 (默认1)
            per_page: 每页条数 (默认10)
            service_type: 服务类型 (可选)
            status: 响应状态 (可选, 0=待处理, 1=已接受, 2=已拒绝, 3=已取消)
        """
        try:
            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=10, type=int)
            service_type = request.args.get('service_type', default='', type=str)
            status = request.args.get('status', default=None, type=int)
            
            # 基础查询：获取所有有效的响应(不包括已取消的)
            query = ServiceResponse.query.filter(ServiceResponse.status != 3)
            
            # 如果指定了服务类型，则通过JOIN获取对应需求的服务类型
            if service_type:
                query = query.join(ServiceNeed).filter(
                    ServiceNeed.service_type.ilike(f'%{service_type}%')
                )
            
            # 按状态筛选
            if status is not None:
                query = query.filter(ServiceResponse.status == status)
            
            # 按创建时间倒序排列(最新的首先)
            query = query.order_by(ServiceResponse.created_at.desc())
            
            # 分页
            paginated = query.paginate(page=page, per_page=per_page, error_out=False)
            responses = paginated.items
            
            # 构建响应数据，包含关联信息
            response_data = []
            for resp in responses:
                need = ServiceNeed.query.get(resp.need_id)
                responder = User.query.get(resp.user_id)
                
                response_data.append({
                    'id': resp.id,
                    'need_id': resp.need_id,
                    'need_subject': need.subject if need else '已删除',
                    'service_type': need.service_type if need else '',
                    'user_id': resp.user_id,
                    'responder_name': responder.real_name if responder else '游客',
                    'responder_phone': responder.phone if responder else '',
                    'content': resp.content,
                    'status': resp.status,
                    'status_text': {
                        0: '待处理',
                        1: '已接受',
                        2: '已拒绝',
                        3: '已取消'
                    }.get(resp.status, '未知'),
                    'created_at': resp.created_at.strftime('%Y-%m-%d %H:%M:%S') if resp.created_at else '',
                    'updated_at': resp.updated_at.strftime('%Y-%m-%d %H:%M:%S') if resp.updated_at else ''
                })
            
            return jsonify({
                "code": 200,
                "data": response_data,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": paginated.total,
                    "pages": paginated.pages
                }
            }), 200
        except Exception as e:
            return jsonify({"code": 500, "msg": f"系统错误: {str(e)}"}), 500
    
    
    @app.route('/api/service-responses/<int:response_id>', methods=['GET'])
    def get_service_response(response_id):
        """获取单个服务响应的详细信息"""
        try:
            resp = ServiceResponse.query.get(response_id)
            
            if not resp:
                return jsonify({"code": 404, "msg": "响应不存在"}), 404
            
            need = ServiceNeed.query.get(resp.need_id)
            responder = User.query.get(resp.user_id)
            need_owner = User.query.get(need.user_id) if need else None
            
            return jsonify({
                "code": 200,
                "data": {
                    'id': resp.id,
                    'need_id': resp.need_id,
                    'need_subject': need.subject if need else '已删除',
                    'need_description': need.description if need else '',
                    'service_type': need.service_type if need else '',
                    'user_id': resp.user_id,
                    'responder_name': responder.real_name if responder else '游客',
                    'responder_phone': responder.phone if responder else '',
                    'content': resp.content,
                    'status': resp.status,
                    'status_text': {
                        0: '待处理',
                        1: '已接受',
                        2: '已拒绝',
                        3: '已取消'
                    }.get(resp.status, '未知'),
                    'need_owner_id': need.user_id if need else None,
                    'need_owner_name': need_owner.real_name if need_owner else '游客',
                    'need_owner_phone': need_owner.phone if need_owner else '',
                    'created_at': resp.created_at.strftime('%Y-%m-%d %H:%M:%S') if resp.created_at else '',
                    'updated_at': resp.updated_at.strftime('%Y-%m-%d %H:%M:%S') if resp.updated_at else ''
                }
            }), 200
        except Exception as e:
            return jsonify({"code": 500, "msg": f"系统错误: {str(e)}"}), 500
    
    
    @app.route('/api/my-service-responses/<int:user_id>', methods=['GET'])
    def get_my_service_responses(user_id):
        """
        获取用户发布的所有服务响应
        即：用户对他人需求的响应列表
        
        参数:
            page: 页码 (默认1)
            per_page: 每页条数 (默认10)
        """
        try:
            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=10, type=int)
            
            # 获取该用户发布的所有响应
            query = ServiceResponse.query.filter_by(user_id=user_id).order_by(
                ServiceResponse.created_at.desc()
            )
            
            paginated = query.paginate(page=page, per_page=per_page, error_out=False)
            responses = paginated.items
            
            response_data = []
            for resp in responses:
                need = ServiceNeed.query.get(resp.need_id)
                
                response_data.append({
                    'id': resp.id,
                    'need_id': resp.need_id,
                    'need_subject': need.subject if need else '已删除',
                    'service_type': need.service_type if need else '',
                    'content': resp.content,
                    'status': resp.status,
                    'status_text': {
                        0: '待处理',
                        1: '已接受',
                        2: '已拒绝',
                        3: '已取消'
                    }.get(resp.status, '未知'),
                    'created_at': resp.created_at.strftime('%Y-%m-%d %H:%M:%S') if resp.created_at else '',
                    'updated_at': resp.updated_at.strftime('%Y-%m-%d %H:%M:%S') if resp.updated_at else ''
                })
            
            return jsonify({
                "code": 200,
                "data": response_data,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": paginated.total,
                    "pages": paginated.pages
                }
            }), 200
        except Exception as e:
            return jsonify({"code": 500, "msg": f"系统错误: {str(e)}"}), 500
    
    @app.route('/api/service-needs/<int:need_id>/responses', methods=['GET'])
    def get_need_responses(need_id):
        """
        获取某个服务需求的所有响应列表
        即：发布者查看自己发布的需求的响应列表
        
        参数:
            need_id: 服务需求ID
            page: 页码 (默认1)
            per_page: 每页条数 (默认10)
        """
        try:
            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=10, type=int)
            
            # 获取该需求的所有响应
            query = ServiceResponse.query.filter_by(need_id=need_id).order_by(
                ServiceResponse.created_at.desc()
            )
            
            paginated = query.paginate(page=page, per_page=per_page, error_out=False)
            responses = paginated.items
            
            response_data = []
            for resp in responses:
                responder = User.query.get(resp.user_id)
                
                response_data.append({
                    'id': resp.id,
                    'need_id': resp.need_id,
                    'user_id': resp.user_id,
                    'responder_name': responder.real_name if responder else '游客',
                    'responder_phone': responder.phone if responder else '',
                    'content': resp.content,
                    'status': resp.status,
                    'status_text': {
                        0: '待处理',
                        1: '已接受',
                        2: '已拒绝',
                        3: '已取消'
                    }.get(resp.status, '未知'),
                    'created_at': resp.created_at.strftime('%Y-%m-%d %H:%M:%S') if resp.created_at else '',
                    'updated_at': resp.updated_at.strftime('%Y-%m-%d %H:%M:%S') if resp.updated_at else ''
                })
            
            return jsonify({
                "code": 200,
                "data": response_data,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": paginated.total,
                    "pages": paginated.pages
                }
            }), 200
        except Exception as e:
            return jsonify({"code": 500, "msg": f"系统错误: {str(e)}"}), 500
    
    
    @app.route('/api/service-responses', methods=['POST'])
    def create_service_response():
        """
        创建新的服务响应
        用户通过此接口对某个需求提出服务响应
        
        请求体:
            {
                "need_id": 1,        # 所响应的需求ID
                "user_id": 2,        # 响应用户ID
                "content": "我可以帮你做..."  # 响应内容
            }
        """
        try:
            data = request.json
            
            # 验证必填字段
            if not all(k in data for k in ['need_id', 'user_id', 'content']):
                return jsonify({"code": 400, "msg": "缺少必填字段"}), 400
            
            # 检查需求是否存在且有效
            need = ServiceNeed.query.get(data['need_id'])
            if not need or need.status != 0:
                return jsonify({"code": 404, "msg": "需求不存在或已失效"}), 404
            
            # 检查用户是否存在
            user = User.query.get(data['user_id'])
            if not user:
                return jsonify({"code": 404, "msg": "用户不存在"}), 404
            
            # 不允许对自己的需求进行响应
            if need.user_id == data['user_id']:
                return jsonify({"code": 400, "msg": "不能对自己的需求进行响应"}), 400
            
            # 检查是否已经响应过(避免重复)
            existing = ServiceResponse.query.filter_by(
                need_id=data['need_id'],
                user_id=data['user_id'],
                status=0  # 只检查未处理的响应
            ).first()
            
            if existing:
                return jsonify({"code": 400, "msg": "您已经对此需求进行过响应"}), 400
            
            # 创建新的响应记录
            new_response = ServiceResponse(
                need_id=data['need_id'],
                user_id=data['user_id'],
                content=data['content'],
                status=0,  # 0 = 待处理
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            db.session.add(new_response)
            db.session.commit()
            
            return jsonify({
                "code": 200,
                "msg": "响应发布成功",
                "data": {
                    "id": new_response.id,
                    "need_id": new_response.need_id,
                    "user_id": new_response.user_id,
                    "content": new_response.content,
                    "status": new_response.status
                }
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"code": 500, "msg": f"系统错误: {str(e)}"}), 500
    
    
    @app.route('/api/service-responses/<int:response_id>', methods=['PUT'])
    def update_service_response(response_id):
        """
        更新服务响应
        只有响应发布者可以更新(修改响应内容或状态)
        需求接收者可以接受/拒绝响应
        
        请求体可包含:
            {
                "user_id": 2,        # 当前操作用户
                "content": "...",    # 更新响应内容(仅发布者可用)
                "status": 1          # 更新状态(0=待处理, 1=接受, 2=拒绝, 3=取消)
            }
        """
        try:
            data = request.json
            resp = ServiceResponse.query.get(response_id)
            
            if not resp:
                return jsonify({"code": 404, "msg": "响应不存在"}), 404
            
            user_id = data.get('user_id')
            
            # 如果要修改内容，必须是响应发布者
            if 'content' in data:
                if resp.user_id != user_id:
                    return jsonify({"code": 403, "msg": "只有响应发布者可以修改内容"}), 403
                
                # 只有待处理状态才能修改内容
                if resp.status != 0:
                    return jsonify({"code": 400, "msg": "只有待处理的响应才能修改"}), 400
                
                resp.content = data['content']
            
            # 更新状态需要特殊权限
            if 'status' in data:
                new_status = data['status']
                need = ServiceNeed.query.get(resp.need_id)
                
                # 状态为1(接受)时，必须由需求发布者操作
                if new_status == 1:
                    if need.user_id != user_id:
                        return jsonify({"code": 403, "msg": "只有需求发布者可以接受响应"}), 403
                    
                    # 检查是否已有其他被接受的响应
                    other_accepted = ServiceResponse.query.filter_by(
                        need_id=resp.need_id,
                        status=1
                    ).filter(ServiceResponse.id != response_id).first()
                    
                    if other_accepted:
                        return jsonify({"code": 400, "msg": "此需求已有被接受的响应"}), 400
                    
                    # 创建ResponseSuccess记录，标记为成功响应
                    from models import ResponseSuccess
                    response_success = ResponseSuccess(
                        need_id=resp.need_id,
                        need_user_id=need.user_id,
                        response_id=resp.id,
                        response_user_id=resp.user_id
                    )
                    db.session.add(response_success)
                    
                    # 只接受当前响应，不自动拒绝其他响应
                    # 让需求发布者手动处理其他响应，避免自动拒绝带来的用户困惑
                    # 业务逻辑：每个需求可以有多个响应，但只能接受一个
                
                # 状态为2(拒绝)时，也必须由需求发布者操作
                elif new_status == 2:
                    if need.user_id != user_id:
                        return jsonify({"code": 403, "msg": "只有需求发布者可以拒绝响应"}), 403
                
                # 状态为3(取消)时，必须由响应发布者操作
                elif new_status == 3:
                    if resp.user_id != user_id:
                        return jsonify({"code": 403, "msg": "只有响应发布者可以取消响应"}), 403
                
                resp.status = new_status
            
            resp.updated_at = datetime.now()
            db.session.commit()
            
            return jsonify({"code": 200, "msg": "更新成功"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"code": 500, "msg": f"系统错误: {str(e)}"}), 500
    
    
    @app.route('/api/service-responses/<int:response_id>', methods=['DELETE'])
    def delete_service_response(response_id):
        """
        删除服务响应(标记为已取消)
        只有响应发布者可以删除自己的响应
        
        请求体:
            {
                "user_id": 2  # 当前用户ID
            }
        """
        try:
            data = request.json
            resp = ServiceResponse.query.get(response_id)
            
            if not resp:
                return jsonify({"code": 404, "msg": "响应不存在"}), 404
            
            # 检查权限
            user_id = data.get('user_id')
            if resp.user_id != user_id:
                return jsonify({"code": 403, "msg": "只有响应发布者可以删除"}), 403
            
            # 已接受的响应不能删除
            if resp.status == 1:
                return jsonify({"code": 400, "msg": "已被接受的响应不能删除"}), 400
            
            # 标记为已取消而不是删除
            resp.status = 3
            resp.updated_at = datetime.now()
            db.session.commit()
            
            return jsonify({"code": 200, "msg": "删除成功"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"code": 500, "msg": f"系统错误: {str(e)}"}), 500
