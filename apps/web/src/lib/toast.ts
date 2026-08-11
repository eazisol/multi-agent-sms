import { toast } from "sonner";

import { ApiError } from "@/lib/api";

type ToastOptions = {
  description?: string;
  duration?: number;
};

export function notifySuccess(title: string, options: ToastOptions = {}) {
  toast.success(title, {
    description: options.description,
    duration: options.duration ?? 3500,
  });
}

export function notifyError(title: string, options: ToastOptions = {}) {
  toast.error(title, {
    description: options.description,
    duration: options.duration ?? 5500,
  });
}

export function notifyWarning(title: string, options: ToastOptions = {}) {
  toast.warning(title, {
    description: options.description,
    duration: options.duration ?? 4500,
  });
}

export function notifyInfo(title: string, options: ToastOptions = {}) {
  toast.info(title, {
    description: options.description,
    duration: options.duration ?? 4000,
  });
}

/** Map API / network failures into a user-facing error toast. */
export function notifyApiError(fallbackTitle: string, err: unknown) {
  if (err instanceof ApiError) {
    notifyError(fallbackTitle, { description: err.problem.message });
    return;
  }
  if (err instanceof Error && err.message) {
    notifyError(fallbackTitle, { description: err.message });
    return;
  }
  notifyError(fallbackTitle, {
    description: "Please try again. If the issue continues, contact your administrator.",
  });
}
