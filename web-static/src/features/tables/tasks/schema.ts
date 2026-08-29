import { Table } from "@/types/table";

export const tasksSchema: Table = {
  name: "tasks",
  columns: [
    { name: "assigned_to", dataType: "integer", isNullable: true, isAutoIncrement: false, maxLength: 0, numericScale: 0, isPrimaryKey: false, isForeignKey: true, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 32 },
    { name: "attachment", dataType: "bytea", isNullable: true, isAutoIncrement: false, maxLength: 0, numericScale: 0, isPrimaryKey: false, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 0 },
    { name: "completed", dataType: "boolean", isNullable: true, isAutoIncrement: false, maxLength: 0, numericScale: 0, isPrimaryKey: false, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 0 },
    { name: "due_date", dataType: "date", isNullable: true, isAutoIncrement: false, maxLength: 0, numericScale: 0, isPrimaryKey: false, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 0 },
    { name: "notes", dataType: "text", isNullable: true, isAutoIncrement: false, maxLength: 0, numericScale: 0, isPrimaryKey: false, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 0 },
    { name: "project_id", dataType: "integer", isNullable: false, isAutoIncrement: false, maxLength: 0, numericScale: 0, isPrimaryKey: false, isForeignKey: true, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 32 },
    { name: "task_id", dataType: "integer", isNullable: false, isAutoIncrement: true, maxLength: 0, numericScale: 0, isPrimaryKey: true, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 32 },
  ],
};