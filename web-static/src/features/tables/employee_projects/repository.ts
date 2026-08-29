
import { apiClient } from "@/api/apiClient";
import { PaginatedResponse } from "@/models/paginatedResponse";
import type { PaginationRequest } from "@/api/paginationRequest";
import { ApiException } from "@/exceptions/apiException";
import { appConfig } from "@/config/appConfig";
import { useMockDb } from "@/stores/mockDbStore";
import { EmployeeProject, type EmployeeProjectJson } from "./model";
import { employee_projectsSchema } from "./schema";


const ENDPOINT = "/employee-projects";
const TABLE = "employee_projects";
const PK = "employeeProjectId";

export const employee_projectsRepository = {
  // ─── Create ──────────────────────────────────
  async create(record: EmployeeProject): Promise<EmployeeProject> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, employee_projectsSchema);
      const inserted = db.insert(TABLE, record.toJson() as unknown as Record<string, unknown>, PK);
      return EmployeeProject.fromJson(inserted);
    }
    return apiClient.post(ENDPOINT, {
      data: record.toJson(),
      fromJson: (json) => EmployeeProject.fromJson(json),
    });
  },

  // ─── Read ────────────────────────────────────
  async getById(id: number): Promise<EmployeeProject> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, employee_projectsSchema);
      const row = db.getById(TABLE, PK, id);
      if (!row) throw new ApiException("Not found", 404);
      return EmployeeProject.fromJson(row);
    }
    return apiClient.get(`${ENDPOINT}/${ id }`, {
      fromJson: (json) => EmployeeProject.fromJson(json),
    });
  },

  async getAll(pagination: PaginationRequest): Promise<PaginatedResponse<EmployeeProject>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, employee_projectsSchema);
      const items = db.getAll(TABLE).map(EmployeeProject.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.getPaginated(ENDPOINT, {
      params: pagination,
      fromJson: (json) => EmployeeProject.fromJson(json),
    });
  },

  async search(
    filters: Record<string, unknown>,
    pagination: PaginationRequest,
  ): Promise<PaginatedResponse<EmployeeProject>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, employee_projectsSchema);
      const items = db
        .getAll(TABLE)
        .filter((row) =>
          Object.entries(filters).every(([key, value]) => row[key] === value),
        )
        .map(EmployeeProject.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.getPaginated(`${ENDPOINT}/search`, {
      params: { ...filters, ...pagination },
      fromJson: (json) => EmployeeProject.fromJson(json),
    });
  },

  // ─── Update ──────────────────────────────────
  async updateById(
    id: number,
    updates: Partial<EmployeeProjectJson>,
  ): Promise<EmployeeProject> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, employee_projectsSchema);
      const updated = db.update(TABLE, PK, id, updates as unknown as Record<string, unknown>);
      if (!updated) throw new ApiException("Not found", 404);
      return EmployeeProject.fromJson(updated);
    }
    return apiClient.put(`${ENDPOINT}/${ id }`, {
      data: updates,
      fromJson: (json) => EmployeeProject.fromJson(json),
    });
  },

  // ─── Delete ──────────────────────────────────
  async deleteById(id: number): Promise<void> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, employee_projectsSchema);
      db.remove(TABLE, PK, id);
      return;
    }
    await apiClient.delete(`${ENDPOINT}/${ id }`);
  },
};
