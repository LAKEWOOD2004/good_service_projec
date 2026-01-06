#!/usr/bin/env python3
"""
简单测试脚本 - 用于验证API是否正常工作
"""

import requests
import json

# 测试登录API
def test_login():
    print("测试登录API...")
    url = "http://127.0.0.1:5000/api/login"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "username": "admin",
        "password": "admin"
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            print("✅ 登录成功")
            return True
        else:
            print(f"❌ 登录失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ 请求出错: {str(e)}")
        return False

# 测试获取概览统计API
def test_overview_stats():
    print("\n测试获取概览统计API...")
    url = "http://127.0.0.1:5000/api/admin/stats/overview"
    
    try:
        response = requests.get(url)
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            print("✅ 获取概览统计成功")
            return True
        else:
            print(f"❌ 获取概览统计失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ 请求出错: {str(e)}")
        return False

# 测试获取月度统计API
def test_monthly_summary():
    print("\n测试获取月度统计API...")
    url = "http://127.0.0.1:5000/api/admin/stats/monthly-summary"
    
    try:
        response = requests.get(url)
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            print("✅ 获取月度统计成功")
            return True
        else:
            print(f"❌ 获取月度统计失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ 请求出错: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== 开始简单API测试 ===")
    
    test_login()
    test_overview_stats()
    test_monthly_summary()
    
    print("\n=== 测试完成 ===")
