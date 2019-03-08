# !/usr/bin/python3.6
# coding:utf-8
"""
-------------------------------------------------
  Author:        fan_zj
  Date：         2019-3-7
-------------------------------------------------
"""

from IMMonitor.db.common import db, Base
import logging


class MsgDetectResult(Base):
    """
    检测结果数据库表头table_header
    ----------------------------------------------------------------------
    id    msg_id    spam_type    result_info   result_ratio   result_label
    ----------------------------------------------------------------------
    ...
    ...
    ----------------------------------------------------------------------
    """

    id = db.Column(db.Integer, primary_key=True)  # 消息id 自动递增
    msg_id = db.Column(db.Integer)
    # msg_type = db.Column(db.Enum('Text', 'Picture'), comment='消息类别，文本或者图像')
    # log_id = db.Column(db.Long)                     # API接口调用时，正确调用生成的唯一标识码，用于问题定位

    # 成功返回信息

    # 审核结果
    # 1：违规 2：疑似或人工审查
    spam_type = db.Column(db.Integer, comment="审核结果状态")  # data, review/reject
    result_info = db.Column(db.String(50), comment="审核结果敏感信息")  # msg, hit
    result_ratio = db.Column(db.Float, comment="审核结果敏感信息得分概率")  # probability, score

    # 敏感信息类别
    # 图片 ：
    # 1：色情、2：性感、3：暴恐、4: 恶心、5：水印码、6：二维码、7：条形码、8：政治人物、9：敏感词
    # 文字：
    # 11: 暴恐违禁，12：文本色情，13：政治敏感，14：恶意推广，15：低俗辱骂，16：低质灌水
    result_label = db.Column(db.Integer, comment="审核结果敏感信息类别")


    @classmethod
    def batch_insert(cls, result_list):
        """
        批量插入检测结果数据
        :param msg_type：消息类型 -- 文本 or 图像
        :param res：传入消息检测返回的结果
        :return:
        """

        insert_list = []
        for result in result_list:
            temp_ins = cls()
            for key in result.keys():
                setattr(temp_ins, key, str(result[key]))
            insert_list.append(temp_ins)
        try:
            db.session.add_all(insert_list)
            db.session.commit()
            return True
        except Exception as err:
            logging.log(logging.ERROR, repr(err))
            return False

    @classmethod
    def get_msg_res(cls, msg_id):
        """
        查询某个消息的检测结果
        :param msg_id: 查询消息所对应的id
        :return: DetectResults
        """

        return cls.query.filter_by(msg_id=msg_id).all()
        # return DetectResults.query.all()
