import { DataType } from "./dataType";

export interface Column {
  name: string;
  isIndex: boolean;
  dataType: DataType | string;
  isUnique: boolean;
  maxLength: number;
  isNullable: boolean;
  subDatatype: string | null;
  numericScale: number;
  isForeignKey: boolean;
  isPrimaryKey: boolean;
  defaultSetting: string;
  isAutoIncrement: boolean;
  numericPrecision: number;
};