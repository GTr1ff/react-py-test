import { Table } from "@/types/table";

export const benefitsSchema: Table = {
  name: "benefits",
  columns: [
    { name: "benefit_id", dataType: "integer", isNullable: false, isAutoIncrement: true, maxLength: 0, numericScale: 0, isPrimaryKey: true, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 32 },
    { name: "benefit_name", dataType: "character varying", isNullable: false, isAutoIncrement: false, maxLength: 100, numericScale: 0, isPrimaryKey: false, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 0 },
    { name: "benefit_type", dataType: "character varying", isNullable: true, isAutoIncrement: false, maxLength: 50, numericScale: 0, isPrimaryKey: false, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 0 },
    { name: "coverage_details", dataType: "jsonb", isNullable: true, isAutoIncrement: false, maxLength: 0, numericScale: 0, isPrimaryKey: false, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 0 },
    { name: "created_at", dataType: "timestamp with time zone", isNullable: true, isAutoIncrement: false, maxLength: 0, numericScale: 0, isPrimaryKey: false, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 0 },
    { name: "monthly_cost", dataType: "numeric", isNullable: true, isAutoIncrement: false, maxLength: 0, numericScale: 2, isPrimaryKey: false, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 10 },
  ],
};