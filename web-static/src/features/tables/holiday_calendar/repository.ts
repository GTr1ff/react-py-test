
import { apiClient } from "@/api/apiClient";
import { PaginatedResponse } from "@/models/paginatedResponse";
import type { PaginationRequest } from "@/api/paginationRequest";
import { ApiException } from "@/exceptions/apiException";
import { appConfig } from "@/config/appConfig";
import { useMockDb } from "@/stores/mockDbStore";
import { HolidayCalendar, type HolidayCalendarJson } from "./model";
import { holiday_calendarSchema } from "./schema";


const ENDPOINT = "/holiday-calendar";
const TABLE = "holiday_calendar";
const PK = "holidayId";

export const holiday_calendarRepository = {
  // ─── Create ──────────────────────────────────
  async create(record: HolidayCalendar): Promise<HolidayCalendar> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, holiday_calendarSchema);
      const inserted = db.insert(TABLE, record.toJson() as unknown as Record<string, unknown>, PK);
      return HolidayCalendar.fromJson(inserted);
    }
    return apiClient.post(ENDPOINT, {
      data: record.toJson(),
      fromJson: (json) => HolidayCalendar.fromJson(json),
    });
  },

  // ─── Read ────────────────────────────────────
  async getById(id: number): Promise<HolidayCalendar> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, holiday_calendarSchema);
      const row = db.getById(TABLE, PK, id);
      if (!row) throw new ApiException("Not found", 404);
      return HolidayCalendar.fromJson(row);
    }
    return apiClient.get(`${ENDPOINT}/${ id }`, {
      fromJson: (json) => HolidayCalendar.fromJson(json),
    });
  },

  async getAll(pagination: PaginationRequest): Promise<PaginatedResponse<HolidayCalendar>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, holiday_calendarSchema);
      const items = db.getAll(TABLE).map(HolidayCalendar.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.getPaginated(ENDPOINT, {
      params: pagination,
      fromJson: (json) => HolidayCalendar.fromJson(json),
    });
  },

  async search(
    filters: Record<string, unknown>,
    pagination: PaginationRequest,
  ): Promise<PaginatedResponse<HolidayCalendar>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, holiday_calendarSchema);
      const items = db
        .getAll(TABLE)
        .filter((row) =>
          Object.entries(filters).every(([key, value]) => row[key] === value),
        )
        .map(HolidayCalendar.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.getPaginated(`${ENDPOINT}/search`, {
      params: { ...filters, ...pagination },
      fromJson: (json) => HolidayCalendar.fromJson(json),
    });
  },

  // ─── Update ──────────────────────────────────
  async updateById(
    id: number,
    updates: Partial<HolidayCalendarJson>,
  ): Promise<HolidayCalendar> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, holiday_calendarSchema);
      const updated = db.update(TABLE, PK, id, updates as unknown as Record<string, unknown>);
      if (!updated) throw new ApiException("Not found", 404);
      return HolidayCalendar.fromJson(updated);
    }
    return apiClient.put(`${ENDPOINT}/${ id }`, {
      data: updates,
      fromJson: (json) => HolidayCalendar.fromJson(json),
    });
  },

  // ─── Delete ──────────────────────────────────
  async deleteById(id: number): Promise<void> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, holiday_calendarSchema);
      db.remove(TABLE, PK, id);
      return;
    }
    await apiClient.delete(`${ENDPOINT}/${ id }`);
  },
};
