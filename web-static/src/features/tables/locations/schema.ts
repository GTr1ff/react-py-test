import { Table } from "@/types/table";

export const locationsSchema: Table = {
  name: "locations",
  columns: [
    { name: "address_line_1", dataType: "character varying", isNullable: true, isAutoIncrement: false, maxLength: 100, numericScale: 0, isPrimaryKey: false, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 0 },
    { name: "address_line_2", dataType: "character varying", isNullable: true, isAutoIncrement: false, maxLength: 100, numericScale: 0, isPrimaryKey: false, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 0 },
    { name: "city", dataType: "character varying", isNullable: true, isAutoIncrement: false, maxLength: 100, numericScale: 0, isPrimaryKey: false, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 0 },
    { name: "country", dataType: "character varying", isNullable: true, isAutoIncrement: false, maxLength: 100, numericScale: 0, isPrimaryKey: false, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 0 },
    { name: "location_id", dataType: "integer", isNullable: false, isAutoIncrement: true, maxLength: 0, numericScale: 0, isPrimaryKey: true, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 32 },
    { name: "location_name", dataType: "character varying", isNullable: true, isAutoIncrement: false, maxLength: 100, numericScale: 0, isPrimaryKey: false, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 0 },
    { name: "state", dataType: "character varying", isNullable: true, isAutoIncrement: false, maxLength: 100, numericScale: 0, isPrimaryKey: false, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 0 },
    { name: "zip_code", dataType: "character varying", isNullable: true, isAutoIncrement: false, maxLength: 20, numericScale: 0, isPrimaryKey: false, isForeignKey: false, isUnique: false, isIndex: false, subDatatype: null, defaultSetting: "", numericPrecision: 0 },
  ],
};