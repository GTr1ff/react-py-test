import { Table } from "@/types/table";

export const leavesSchema: Table = {
  name: "leaves",
  columns: [
    { name: "approval_status", dataType: "character varying", isNullable: true, isAutoIncrement: false, maxLength: 20, numericScale: 0, isPrimaryKey: false, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 0 },
    { name: "approved_by", dataType: "integer", isNullable: true, isAutoIncrement: false, maxLength: 0, numericScale: 0, isPrimaryKey: false, isForeignKey: true, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 32 },
    { name: "employee_id", dataType: "integer", isNullable: false, isAutoIncrement: false, maxLength: 0, numericScale: 0, isPrimaryKey: false, isForeignKey: true, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 32 },
    { name: "end_date", dataType: "date", isNullable: false, isAutoIncrement: false, maxLength: 0, numericScale: 0, isPrimaryKey: false, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 0 },
    { name: "leave_id", dataType: "integer", isNullable: false, isAutoIncrement: true, maxLength: 0, numericScale: 0, isPrimaryKey: true, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 32 },
    { name: "reason", dataType: "text", isNullable: true, isAutoIncrement: false, maxLength: 0, numericScale: 0, isPrimaryKey: false, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 0 },
    { name: "start_date", dataType: "date", isNullable: false, isAutoIncrement: false, maxLength: 0, numericScale: 0, isPrimaryKey: false, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 0 },
  ],
};