
export interface DatatypestestJson {
  bigintCol: number | null;
  booleanCol: boolean | null;
  byteaCol: string | null;
  charCol: string | null;
  dateCol: string | null;
  decimalCol: string | null;
  doublePrecisionCol: number | null;
  intArrayCol: unknown | null;
  integerCol: number | null;
  keykey: number;
  moneyCol: string | null;
  numericCol: string | null;
  realCol: number | null;
  smallintCol: number | null;
  textArrayCol: unknown | null;
  textCol: string | null;
  timeCol: string | null;
  timestampCol: string | null;
  timestamptzCol: string | null;
  timetzCol: string | null;
  varcharCol: string | null;
}

export class Datatypestest {
  constructor(
    public readonly bigintCol: number | null,
    public readonly booleanCol: boolean | null,
    public readonly byteaCol: string | null,
    public readonly charCol: string | null,
    public readonly dateCol: string | null,
    public readonly decimalCol: string | null,
    public readonly doublePrecisionCol: number | null,
    public readonly intArrayCol: unknown | null,
    public readonly integerCol: number | null,
    public readonly keykey: number,
    public readonly moneyCol: string | null,
    public readonly numericCol: string | null,
    public readonly realCol: number | null,
    public readonly smallintCol: number | null,
    public readonly textArrayCol: unknown | null,
    public readonly textCol: string | null,
    public readonly timeCol: string | null,
    public readonly timestampCol: string | null,
    public readonly timestamptzCol: string | null,
    public readonly timetzCol: string | null,
    public readonly varcharCol: string | null,
  ) {}

  static fromJson(json: unknown): Datatypestest {
    const data = json as DatatypestestJson;
    return new Datatypestest(
      data.bigintCol,
      data.booleanCol,
      data.byteaCol,
      data.charCol,
      data.dateCol,
      data.decimalCol,
      data.doublePrecisionCol,
      data.intArrayCol,
      data.integerCol,
      data.keykey,
      data.moneyCol,
      data.numericCol,
      data.realCol,
      data.smallintCol,
      data.textArrayCol,
      data.textCol,
      data.timeCol,
      data.timestampCol,
      data.timestamptzCol,
      data.timetzCol,
      data.varcharCol,
    );
  }

  toJson(): DatatypestestJson {
    return {
      bigintCol: this.bigintCol,
      booleanCol: this.booleanCol,
      byteaCol: this.byteaCol,
      charCol: this.charCol,
      dateCol: this.dateCol,
      decimalCol: this.decimalCol,
      doublePrecisionCol: this.doublePrecisionCol,
      intArrayCol: this.intArrayCol,
      integerCol: this.integerCol,
      keykey: this.keykey,
      moneyCol: this.moneyCol,
      numericCol: this.numericCol,
      realCol: this.realCol,
      smallintCol: this.smallintCol,
      textArrayCol: this.textArrayCol,
      textCol: this.textCol,
      timeCol: this.timeCol,
      timestampCol: this.timestampCol,
      timestamptzCol: this.timestamptzCol,
      timetzCol: this.timetzCol,
      varcharCol: this.varcharCol,
    };
  }
}