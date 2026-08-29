
export interface HolidayCalendarJson {
  holidayDate: string;
  holidayId: number;
  holidayName: string;
  isNational: boolean | null;
}

export class HolidayCalendar {
  constructor(
    public readonly holidayDate: string,
    public readonly holidayId: number,
    public readonly holidayName: string,
    public readonly isNational: boolean | null,
  ) {}

  static fromJson(json: unknown): HolidayCalendar {
    const data = json as HolidayCalendarJson;
    return new HolidayCalendar(
      data.holidayDate,
      data.holidayId,
      data.holidayName,
      data.isNational,
    );
  }

  toJson(): HolidayCalendarJson {
    return {
      holidayDate: this.holidayDate,
      holidayId: this.holidayId,
      holidayName: this.holidayName,
      isNational: this.isNational,
    };
  }
}