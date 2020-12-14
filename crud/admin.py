from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from crud.models import Student, Transaction, Fees, Course, Organization


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('enr_no',)


@admin.register(Transaction)
class TransactionAdmin(ImportExportModelAdmin):
    save_as = True
    list_display = ('id', 'transaction_id', 'order_id', 'amount', 'bank_name', 'm_id')
    list_editable = ('transaction_id', 'order_id', 'amount', 'bank_name', 'm_id')
    list_filter = ('order_id', 'transaction_id')
    search_fields = ('order_id', 'transaction_id')


@admin.register(Fees)
class FeesAdmin(admin.ModelAdmin):
    list_display = ('id', 'organization', 'course', 'fee')
    list_filter = ('organization',)
    list_editable = ('fee',)


class FeesInline(admin.TabularInline):
    model = Fees


class CourseAdmin(admin.ModelAdmin):
    inlines = (FeesInline,)
    # fields = ('get_organizations', 'name', 'description')
    list_display = ('id', 'name', 'description')
    # list_editable = ('description',)
    list_filter = ('name', 'organization')
    # ordering = ('name',)
    # search_fields = ('name_startswith',)


admin.site.register(Course, CourseAdmin)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    save_as = True
    fields = ('name', 'description', 'contact', 'email')
    list_display = ('id', 'name', 'description', 'contact', 'email')
    list_editable = ('description',)
    list_filter = ('name',)
    ordering = ('name',)
    search_fields = ('name_startswith',)
