
import { apiClient } from "@/api/apiClient";
import { PaginatedResponse } from "@/models/paginatedResponse";
import type { PaginationRequest } from "@/api/paginationRequest";
import { ApiException } from "@/exceptions/apiException";
import { appConfig } from "@/config/appConfig";
import { useMockDb } from "@/stores/mockDbStore";
import { EmployeeBenefit, type EmployeeBenefitJson } from "./model";
import { employee_benefitsSchema } from "./schema";


const ENDPOINT = "/employee-benefits";
const TABLE = "employee_benefits";
const PK = "employeeBenefitId";

export const employee_benefitsRepository = {
  // ─── Create ──────────────────────────────────
  async create(record: EmployeeBenefit): Promise<EmployeeBenefit> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, employee_benefitsSchema);
      const inserted = db.insert(TABLE, record.toJson() as unknown as Record<string, unknown>, PK);
      return EmployeeBenefit.fromJson(inserted);
    }
    return apiClient.post(ENDPOINT, {
      data: record.toJson(),
      fromJson: (json) => EmployeeBenefit.fromJson(json),
    });
  },

  // ─── Read ────────────────────────────────────
  async getById(id: number): Promise<EmployeeBenefit> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, employee_benefitsSchema);
      const row = db.getById(TABLE, PK, id);
      if (!row) throw new ApiException("Not found", 404);
      return EmployeeBenefit.fromJson(row);
    }
    return apiClient.get(`${ENDPOINT}/${ id }`, {
      fromJson: (json) => EmployeeBenefit.fromJson(json),
    });
  },

  async getAll(pagination: PaginationRequest): Promise<PaginatedResponse<EmployeeBenefit>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, employee_benefitsSchema);
      const items = db.getAll(TABLE).map(EmployeeBenefit.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.getPaginated(ENDPOINT, {
      params: pagination,
      fromJson: (json) => EmployeeBenefit.fromJson(json),
    });
  },

  async search(
    filters: Record<string, unknown>,
    pagination: PaginationRequest,
  ): Promise<PaginatedResponse<EmployeeBenefit>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, employee_benefitsSchema);
      const items = db
        .getAll(TABLE)
        .filter((row) =>
          Object.entries(filters).every(([key, value]) => row[key] === value),
        )
        .map(EmployeeBenefit.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.getPaginated(`${ENDPOINT}/search`, {
      params: { ...filters, ...pagination },
      fromJson: (json) => EmployeeBenefit.fromJson(json),
    });
  },

  // ─── Update ──────────────────────────────────
  async updateById(
    id: number,
    updates: Partial<EmployeeBenefitJson>,
  ): Promise<EmployeeBenefit> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, employee_benefitsSchema);
      const updated = db.update(TABLE, PK, id, updates as unknown as Record<string, unknown>);
      if (!updated) throw new ApiException("Not found", 404);
      return EmployeeBenefit.fromJson(updated);
    }
    return apiClient.put(`${ENDPOINT}/${ id }`, {
      data: updates,
      fromJson: (json) => EmployeeBenefit.fromJson(json),
    });
  },

  // ─── Delete ──────────────────────────────────
  async deleteById(id: number): Promise<void> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, employee_benefitsSchema);
      db.remove(TABLE, PK, id);
      return;
    }
    await apiClient.delete(`${ENDPOINT}/${ id }`);
  },
};
