# -*- coding: utf-8 -*-
import uvicorn
from core.server import create_app

app = create_app()


if __name__ == '__main__':
    # 输出所有的路由
    for route in app.routes:
        if hasattr(route, "methods"):
            print({'path': route.path, 'name': route.name, 'methods': route.methods})
    uvicorn.run(app='run:app', host='0.0.0.0', port=8011)
