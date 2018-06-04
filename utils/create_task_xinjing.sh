#!/bin/bash
# sudo -u postgres psql <<END
# drop database if exists tripitaka_platform;
# drop user if exists lqzj;
# END
# sudo -u postgres psql -f utils/setup_db.sql
sudo ./manage.py reset_db

rm -f tdata/migrations/000*
rm -f tasks/migrations/000*
rm -f rect/migrations/000*
./manage.py makemigrations tdata
./manage.py makemigrations tasks
./manage.py makemigrations rect
cp rect/sql/*.py rect/migrations/.
./manage.py migrate
./manage.py create_configuration
./manage.py import_tripitaka_list

# 导入cbeta底本数据. 为心经
./manage.py import_cbeta_base
#将藏经版本的cut_ready设置为True
./manage.py set_cut_ready

# 根据LQSutra的信息(total_reels)去创建龙泉卷实例, 用reel_no与其他藏经的卷关联吧?
./manage.py create_lqreel

#根据已导入的藏经卷信息生成卷的path1,2,3信息, 方便后续组合S3的访问路径.
./manage.py generate_reel_path

#下载GL高丽藏每一卷的文本数据, 解析到对就高丽藏经的卷, 再对应ReelCorrectText校对文本信息中(head, body, tail).
./manage.py import_reel_xinjing
./manage.py import_gl_xinjing

#从'data/ocr_ready_list.txt'<YB000860_011>文件获取并判断卷的ocr数据是否准备了,
# 并找到相应的卷信息更新它的ocr_ready=True
#./manage.py import_ocr_ready_list  #在import_reel_xinjing中解析cut时设置
./manage.py create_reel_and_tasks
