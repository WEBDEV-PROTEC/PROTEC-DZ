# -*- coding: utf-8 -*-
# from odoo import http


# class VideoPlayer(http.Controller):
#     @http.route('/video_player/video_player/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/video_player/video_player/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('video_player.listing', {
#             'root': '/video_player/video_player',
#             'objects': http.request.env['video_player.video_player'].search([]),
#         })

#     @http.route('/video_player/video_player/objects/<model("video_player.video_player"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('video_player.object', {
#             'object': obj
#         })
