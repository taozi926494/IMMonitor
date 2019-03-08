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

    id = db.Column(db.Integer, primary_key=True, auto_increment=True)    # 消息id 自动递增
    msg_id = db.Column(db.Integer)
    # msg_type = db.Column(db.Enum('Text', 'Picture'), comment='消息类别，文本或者图像')
    # log_id = db.Column(db.Long)                     # API接口调用时，正确调用生成的唯一标识码，用于问题定位

    # 成功返回信息
    spam_type = db.Column(db.String(20), comment="审核结果状态")  # data, review/reject
    result_info = db.Column(db.String(50), comment="审核结果敏感信息")  # msg, hit
    result_ratio = db.Column(db.float, comment="审核结果敏感信息得分概率")  # probability, score
    result_label = db.Column(db.String(20), comment="审核结果敏感信息类别")   # type, label

    # # 文本检测结果
    # text_spam = db.Column(db.Integer)               # 是否包含违禁，0表示非违禁，1表示违禁，2表示建议人工复审
    # text_reject = db.Column(db.Dict)                # 审核未通过的类别列表与详情
    # text_review = db.Column(db.Dict)                # 待人工复审的类别列表与详情
    # text_pass = db.Column(db.Dict)                  # 审核通过的类别列表与详情
    # # 图像检测结果
    # image_conclusion = db.Column(db.String(20))     # 审核结果描述，成功才返回，失败不返回。可取值 1.合规, 2.不合规, 3.疑似, 4.审核失败
    # # 审核类型，1：色情、2：性感、3：暴恐、4:恶心、5：水印码、# 6：二维码、7：条形码、8：政治人物、9：敏感词、10：自定义敏感词
    # image_conclusion_type = db.Column(db.String(20))
    # image_conclusion_data = db.Column(db.Dict)      # 审核项详细信息，响应成功并且conclusion为疑似或不合规时才返回，响应失败或conclusion为合规是不返回。
    # image_conclusion_data_stars = db.Column(db.Dict)

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
