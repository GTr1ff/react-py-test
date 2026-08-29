import { Table } from "@/types/table";

export const salariesSchema: Table = {
  name: "salaries",
  columns: [
    { name: "currency", dataType: "character varying", isNullable: false, isAutoIncrement: false, maxLength: 3, numericScale: 0, isPrimaryKey: false, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 0 },
    { name: "effective_date", dataType: "date", isNullable: false, isAutoIncrement: false, maxLength: 0, numericScale: 0, isPrimaryKey: false, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 0 },
    { name: "employee_id", dataType: "integer", isNullable: false, isAutoIncrement: false, maxLength: 0, numericScale: 0, isPrimaryKey: false, isForeignKey: true, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 32 },
    { name: "salary", dataType: "numeric", isNullable: false, isAutoIncrement: false, maxLength: 0, numericScale: 2, isPrimaryKey: false, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 10 },
    { name: "salary_id", dataType: "integer", isNullable: false, isAutoIncrement: true, maxLength: 0, numericScale: 0, isPrimaryKey: true, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 32 },
  ],
};