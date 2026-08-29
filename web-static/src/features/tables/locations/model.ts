
export interface LocationJson {
  addressLine_1: string | null;
  addressLine_2: string | null;
  city: string | null;
  country: string | null;
  locationId: number;
  locationName: string | null;
  state: string | null;
  zipCode: string | null;
}

export class Location {
  constructor(
    public readonly addressLine_1: string | null,
    public readonly addressLine_2: string | null,
    public readonly city: string | null,
    public readonly country: string | null,
    public readonly locationId: number,
    public readonly locationName: string | null,
    public readonly state: string | null,
    public readonly zipCode: string | null,
  ) {}

  static fromJson(json: unknown): Location {
    const data = json as LocationJson;
    return new Location(
      data.addressLine_1,
      data.addressLine_2,
      data.city,
      data.country,
      data.locationId,
      data.locationName,
      data.state,
      data.zipCode,
    );
  }

  toJson(): LocationJson {
    return {
      addressLine_1: this.addressLine_1,
      addressLine_2: this.addressLine_2,
      city: this.city,
      country: this.country,
      locationId: this.locationId,
      locationName: this.locationName,
      state: this.state,
      zipCode: this.zipCode,
    };
  }
}