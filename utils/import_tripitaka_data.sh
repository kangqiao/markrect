#!/bin/bash

sid="LQ003900"
if [ "$1" != '' ]; then
    sid=$1
fi

# 清空数据库, 需要用户权限
sudo ./manage.py reset_db

# 清除业务模块的migrations
rm -f tdata/migrations/000*
rm -f segment/migrations/000*
# 重新构建数据库.
./manage.py makemigrations tdata
./manage.py makemigrations segment
./manage.py migrate

# 创建异体字库 => tdata.models.Configuration
./manage.py create_configuration
# 导入藏经列表 => tdata.models.Tripitaka
./manage.py import_tripitaka_list

# 导入用户, 权限, 角色, 菜单,  => jwt_auth.models.*
./manage.py loaddata ./data/initial_fixtures/demo_auth.json
###./manage.py create_xadmin_bookmark

# 导入指定龙泉经目 => data/sutra_list/lqsutra.txt
./manage.py import_lqsutra $sid
# 创建指定龙泉经目的卷列表数据 => tdata.models.LQReel
./manage.py create_lqreel $sid

# 导入各藏经版本经目卷目信息 => data/sutra_list/sutra_list.txt , data/sutra_list/reel_list.txt
./manage.py import_sutra
# 导入指定经目的卷信息. => data/reel_info/$sid.txt
./manage.py import_reel $sid

# 生成卷路径 => path1(vid or sid), path2(reel_no)
./manage.py generate_reel_path

# 生成页数据.

# 生成待标注的PageRect数据项
./manage.py create_segment_pagerect $sid











# 导入cbeta底本数据. 为心经
#./manage.py import_cbeta_base
#将藏经版本的cut_ready设置为True
#./manage.py set_cut_ready

# 根据LQSutra的信息(total_reels)去创建龙泉卷实例, 用reel_no与其他藏经的卷关联吧?
#./manage.py create_lqreel

#根据已导入的藏经卷信息生成卷的path1,2,3信息, 方便后续组合S3的访问路径.
#./manage.py generate_reel_path

#下载GL高丽藏每一卷的文本数据, 解析到对就高丽藏经的卷, 再对应ReelCorrectText校对文本信息中(head, body, tail).
#./manage.py import_reel_xinjing
#./manage.py import_gl_xinjing

#从'data/ocr_ready_list.txt'<YB000860_011>文件获取并判断卷的ocr数据是否准备了,
# 并找到相应的卷信息更新它的ocr_ready=True
#./manage.py import_ocr_ready_list  #在import_reel_xinjing中解析cut时设置
#./manage.py create_reel_and_tasks
