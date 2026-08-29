# ROSETIC:crud-guid



from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from features.tables.salaries.models import SalaryModel
    from features.tables.employee_benefits.models import EmployeeBenefitModel
    from features.tables.tasks.models import TaskModel
    from features.tables.leaves.models import LeafModel
    from features.tables.leaves.models import LeafModel
    from features.tables.job_history.models import JobHistoryModel
    from features.tables.performance_reviews.models import PerformanceReviewModel
    from features.tables.payroll.models import PayrollModel
    from features.tables.time_logs.models import TimeLogModel
    from features.tables.documents.models import DocumentModel
    from features.tables.employee_projects.models import EmployeeProjectModel
    from features.tables.departments.models import DepartmentModel

import sqlalchemy

import datetime
from dataclasses import Field
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class EmployeeModel(Base):

    __tablename__ = "employees"
    __default_sort__ = "employee_id"

    employee_id: Mapped[int] = mapped_column(
        sqlalchemy.Integer,
        primary_key=True, 
        autoincrement=True
    )

    birth_date: Mapped[datetime.date | None] = mapped_column(
        sqlalchemy.Date,
        nullable=True
    )
    created_at: Mapped[datetime.datetime | None] = mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=True,
        server_default=sqlalchemy.func.now()
    )
    department_id: Mapped[int | None] = mapped_column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("departments.department_id")
    )
    department_id_department: Mapped[DepartmentModel| None] = relationship(
        back_populates="employees_by_department_id", 
        lazy="noload",
        remote_side="DepartmentModel.department_id",
        foreign_keys=[department_id]
    )
    
    email: Mapped[str | None] = mapped_column(
        sqlalchemy.String(100),
        nullable=True
    )
    first_name: Mapped[str] = mapped_column(
        sqlalchemy.String(50),
        nullable=False
    )
    hire_date: Mapped[datetime.date] = mapped_column(
        sqlalchemy.Date,
        nullable=False
    )
    is_active: Mapped[bool | None] = mapped_column(
        sqlalchemy.Boolean,
        nullable=True,
        server_default=sqlalchemy.text("true")
    )
    last_name: Mapped[str] = mapped_column(
        sqlalchemy.String(50),
        nullable=False
    )
    phone: Mapped[str | None] = mapped_column(
        sqlalchemy.String(20),
        nullable=True
    )
    updated_at: Mapped[datetime.datetime | None] = mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=True,
        server_default=sqlalchemy.func.now(),
        onupdate=sqlalchemy.func.now()
    )

    # Child relationships

    salaries_by_employee_id: Mapped[list[SalaryModel]] = relationship(
        back_populates="employee_id_employee",
        lazy="noload",
        foreign_keys="SalaryModel.employee_id"
    )
    employee_benefits_by_employee_id: Mapped[list[EmployeeBenefitModel]] = relationship(
        back_populates="employee_id_employee",
        lazy="noload",
        foreign_keys="EmployeeBenefitModel.employee_id"
    )
    tasks_by_assigned_to: Mapped[list[TaskModel]] = relationship(
        back_populates="assigned_to_employee",
        lazy="noload",
        foreign_keys="TaskModel.assigned_to"
    )
    leaves_by_employee_id: Mapped[list[LeafModel]] = relationship(
        back_populates="employee_id_employee",
        lazy="noload",
        foreign_keys="LeafModel.employee_id"
    )
    leaves_by_approved_by: Mapped[list[LeafModel]] = relationship(
        back_populates="approved_by_employee",
        lazy="noload",
        foreign_keys="LeafModel.approved_by"
    )
    job_history_by_employee_id: Mapped[list[JobHistoryModel]] = relationship(
        back_populates="employee_id_employee",
        lazy="noload",
        foreign_keys="JobHistoryModel.employee_id"
    )
    performance_reviews_by_employee_id: Mapped[list[PerformanceReviewModel]] = relationship(
        back_populates="employee_id_employee",
        lazy="noload",
        foreign_keys="PerformanceReviewModel.employee_id"
    )
    payroll_by_employee_id: Mapped[list[PayrollModel]] = relationship(
        back_populates="employee_id_employee",
        lazy="noload",
        foreign_keys="PayrollModel.employee_id"
    )
    time_logs_by_employee_id: Mapped[list[TimeLogModel]] = relationship(
        back_populates="employee_id_employee",
        lazy="noload",
        foreign_keys="TimeLogModel.employee_id"
    )
    documents_by_employee_id: Mapped[list[DocumentModel]] = relationship(
        back_populates="employee_id_employee",
        lazy="noload",
        foreign_keys="DocumentModel.employee_id"
    )
    employee_projects_by_employee_id: Mapped[list[EmployeeProjectModel]] = relationship(
        back_populates="employee_id_employee",
        lazy="noload",
        foreign_keys="EmployeeProjectModel.employee_id"
    )
