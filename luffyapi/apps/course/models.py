from django.db import models
from luffyapi.utils.models import BaseModel

"""
课程表-免费课
"""


class CourseCategory(BaseModel):
    """分类"""
    name = models.CharField(max_length=64, unique=True, verbose_name="分类名称")

    class Meta:
        db_table = "luffy_course_category"  # 修改表名
        verbose_name = "分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % self.name


class Course(BaseModel):
    """课程"""
    course_type = (
        (0, '付费'),
        (1, 'VIP专享'),
        (2, '学位课程')
    )
    level_choices = (
        (0, '初级'),
        (1, '中级'),
        (2, '高级'),
    )
    status_choices = (
        (0, '上线'),
        (1, '下线'),
        (2, '预上线'),
    )
    name = models.CharField(max_length=128, verbose_name="课程名称")
    course_img = models.ImageField(upload_to="courses", max_length=255, verbose_name="封面图片", blank=True, null=True)
    course_type = models.SmallIntegerField(choices=course_type, default=0, verbose_name="付费类型")
    # 使用这个字段的原因
    brief = models.TextField(max_length=2048, verbose_name="详情介绍", null=True, blank=True)
    level = models.SmallIntegerField(choices=level_choices, default=0, verbose_name="难度等级")
    pub_date = models.DateField(verbose_name="发布日期", auto_now_add=True)
    period = models.IntegerField(verbose_name="建议学习周期(day)", default=7)
    attachment_path = models.FileField(upload_to="attachment", max_length=128, verbose_name="课件路径", blank=True,
                                       null=True)
    status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name="课程状态")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="课程原价", default=0)

    # 字段优化
    sections = models.IntegerField(verbose_name="总课时数量", default=0)
    students = models.IntegerField(verbose_name="学习人数", default=0)
    pub_sections = models.IntegerField(verbose_name="课时更新数量", default=0)

    # 外键
    teacher = models.ForeignKey("Teacher", on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="授课老师",
                                db_constraint=False)
    course_category = models.ForeignKey("CourseCategory", on_delete=models.SET_NULL, db_constraint=False, null=True,
                                        blank=True,
                                        verbose_name="课程分类")

    class Meta:
        db_table = "luffy_course"
        verbose_name = "课程"
        verbose_name_plural = "课程"

    def __str__(self):
        return "%s" % self.name

    @property
    def course_type_name(self):
        # 返回role对应中文
        return self.get_course_type_display()

    @property
    def level_name(self):
        return self.get_level_display()

    @property
    def status_name(self):
        return self.get_status_display()

    @property
    def section_list(self):
        # 检索所以章节所以课时，返回前4课时，不足4课时全部返回
        temp_section_list = []

        for chapter in self.coursechapters.all():
            for section in chapter.coursesections.all():
                temp_section_list.append({
                    'name': section.name,
                    'section_link': section.section_link,
                    'duration': section.duration,
                    'free_trail': section.free_trail,
                })
                if len(temp_section_list) >= 4:
                    return temp_section_list  # 最多4条

        return temp_section_list  # 不足4条


class Teacher(BaseModel):
    """导师"""
    role_choices = (
        (0, '讲师'),
        (1, '导师'),
        (2, '班主任'),
    )
    name = models.CharField(max_length=32, verbose_name="导师名")
    role = models.SmallIntegerField(choices=role_choices, default=0, verbose_name="导师身份")
    title = models.CharField(max_length=64, verbose_name="职位、职称")
    signature = models.CharField(max_length=255, verbose_name="导师签名", help_text="导师签名", blank=True, null=True)
    image = models.ImageField(upload_to="teacher", null=True, verbose_name="导师封面")
    brief = models.TextField(max_length=1024, verbose_name="导师简介")

    class Meta:
        db_table = "luffy_teacher"
        verbose_name = "导师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % self.name

    @property
    def role_name(self):
        # 返回role对应中文
        return self.get_role_display()



class CourseChapter(BaseModel):
    """章节"""
    chapter = models.SmallIntegerField(verbose_name="第几章", default=1)
    name = models.CharField(max_length=128, verbose_name="章节标题")
    summary = models.TextField(verbose_name="章节介绍", blank=True, null=True)
    pub_date = models.DateField(verbose_name="发布日期", auto_now_add=True)

    # 外键：一（课程）对多（章节）
    course = models.ForeignKey("Course", related_name='coursechapters', on_delete=models.CASCADE, verbose_name="课程名称")

    class Meta:
        db_table = "luffy_course_chapter"
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s:(第%s章)%s" % (self.course, self.chapter, self.name)


class CourseSection(BaseModel):
    """课时"""
    section_type_choices = (
        (0, '文档'),
        (1, '练习'),
        (2, '视频')
    )

    name = models.CharField(max_length=128, verbose_name="课时标题")
    orders = models.PositiveSmallIntegerField(verbose_name="课时排序")
    section_type = models.SmallIntegerField(default=2, choices=section_type_choices, verbose_name="课时种类")
    section_link = models.CharField(max_length=255, blank=True, null=True, verbose_name="课时链接",
                                    help_text="若是video，填vid,若是文档，填link")
    duration = models.CharField(verbose_name="视频时长", blank=True, null=True, max_length=32)  # 仅在前端展示使用
    pub_date = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)
    free_trail = models.BooleanField(verbose_name="是否可试看", default=False)

    # 外键
    chapter = models.ForeignKey("CourseChapter", related_name='coursesections', on_delete=models.CASCADE,
                                verbose_name="课程章节")

    class Meta:
        db_table = "luffy_course_Section"
        verbose_name = "课时"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s-%s" % (self.chapter, self.name)
