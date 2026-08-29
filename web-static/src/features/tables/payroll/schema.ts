import { Table } from "@/types/table";

export const payrollSchema: Table = {
  name: "payroll",
  columns: [
    { name: "employee_id", dataType: "integer", isNullable: false, isAutoIncrement: false, maxLength: 0, numericScale: 0, isPrimaryKey: false, isForeignKey: true, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 32 },
    { name: "hours_worked", dataType: "numeric", isNullable: true, isAutoIncrement: false, maxLength: 0, numericScale: 2, isPrimaryKey: false, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 5 },
    { name: "pay_period_end", dataType: "date", isNullable: false, isAutoIncrement: false, maxLength: 0, numericScale: 0, isPrimaryKey: false, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 0 },
    { name: "pay_period_start", dataType: "date", isNullable: false, isAutoIncrement: false, maxLength: 0, numericScale: 0, isPrimaryKey: false, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 0 },
    { name: "payroll_id", dataType: "integer", isNullable: false, isAutoIncrement: true, maxLength: 0, numericScale: 0, isPrimaryKey: true, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 32 },
    { name: "wages", dataType: "numeric", isNullable: true, isAutoIncrement: false, maxLength: 0, numericScale: 2, isPrimaryKey: false, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 10 },
  ],
};