import { Table } from "@/types/table";

export const projectsSchema: Table = {
  name: "projects",
  columns: [
    { name: "budget", dataType: "numeric", isNullable: true, isAutoIncrement: false, maxLength: 0, numericScale: 2, isPrimaryKey: false, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 12 },
    { name: "created_at", dataType: "timestamp with time zone", isNullable: true, isAutoIncrement: false, maxLength: 0, numericScale: 0, isPrimaryKey: false, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 0 },
    { name: "end_date", dataType: "date", isNullable: true, isAutoIncrement: false, maxLength: 0, numericScale: 0, isPrimaryKey: false, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 0 },
    { name: "project_id", dataType: "integer", isNullable: false, isAutoIncrement: true, maxLength: 0, numericScale: 0, isPrimaryKey: true, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 32 },
    { name: "project_name", dataType: "character varying", isNullable: false, isAutoIncrement: false, maxLength: 200, numericScale: 0, isPrimaryKey: false, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 0 },
    { name: "start_date", dataType: "date", isNullable: true, isAutoIncrement: false, maxLength: 0, numericScale: 0, isPrimaryKey: false, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 0 },
    { name: "status", dataType: "character varying", isNullable: false, isAutoIncrement: false, maxLength: 50, numericScale: 0, isPrimaryKey: false, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 0 },
    { name: "tags", dataType: "ARRAY", isNullable: true, isAutoIncrement: false, maxLength: 0, numericScale: 0, isPrimaryKey: false, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 0 },
  ],
};