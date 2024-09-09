import React, { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { useNavigate } from "react-router-dom";
import { Input } from "../components/Input";
import { Textarea } from "../components/Textarea";
import { Button } from "../components/ui/Button";
import { Select } from "../components/Select";
import Cookies from "js-cookie";

// Form schema validation with detailed error messages
const formSchema = z.object({
  username: z.string().min(3, "Username must be at least 3 characters").max(20, "Username cannot exceed 20 characters"),
  email: z.string().email("Please enter a valid email address"),
  password: z.string().min(6, "Password must be at least 6 characters"),
  contact_number: z.string().regex(/^\d{10}$/, "Contact number must be a 10-digit number"),
  full_name: z.string().min(2, "Full name must be at least 2 characters"),
  profile_picture: z.string().url("Please enter a valid URL for the profile picture"),
  job_title: z.string().nonempty("Job title is required"),
  department: z.string().min(1, "Please select a department").nonempty("Required"),
  location: z.string().nonempty("Location is required"),
  short_bio: z.string().max(200, "Bio must be under 200 characters"),
});

export default function AddUserForm() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(""); // To handle token error
  const navigate = useNavigate(); // For redirecting after form submission

  const form = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: {
      username: "",
      email: "",
      password: "",
      contact_number: "",
      full_name: "",
      profile_picture: "",
      job_title: "",
      department: "",
      location: "",
      short_bio: "",
    },
  });

  // Check if token exists on component mount
  useEffect(() => {
    const token = Cookies.get("auth_token");
    if (!token) {
      setError("You are not allowed to access this page. Redirecting to signup...");
      setTimeout(() => {
        navigate("/signup"); // Redirect after 2 seconds
      }, 2000);
    }
  }, [navigate]);

  async function onSubmit(values) {
    setIsLoading(true);
    try {
      const token = Cookies.get("auth_token");
      if (!token) {
        throw new Error("Authorization token is missing");
      }

      const response = await fetch("http://localhost:8000/api/add_user/", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(values),
      });

      if (!response.ok) {
        throw new Error("Failed to add user");
      }

      alert("User added successfully!");
      navigate("/users");
    } catch (error) {
      alert(error.message || "Failed to add user. Please try again.");
    } finally {
      setIsLoading(false);
    }
  }

  if (error) {
    return (
      <div className="container mx-auto p-4">
        <p className="text-red-500">{error}</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4 max-w-lg">
      <h1 className="text-3xl font-bold mb-6">Add New User</h1>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        <Input
          label="Username"
          {...form.register("username")}
          placeholder="alice_johnson"
          error={form.formState.errors.username?.message}
        />
        <Input
          label="Email"
          type="email"
          {...form.register("email")}
          placeholder="alice@example.com"
          error={form.formState.errors.email?.message}
        />
        <Input
          label="Password"
          type="password"
          {...form.register("password")}
          placeholder="••••••"
          error={form.formState.errors.password?.message}
        />
        <Input
          label="Contact Number"
          {...form.register("contact_number")}
          placeholder="5551234567"
          error={form.formState.errors.contact_number?.message}
        />
        <Input
          label="Full Name"
          {...form.register("full_name")}
          placeholder="Alice Johnson"
          error={form.formState.errors.full_name?.message}
        />
        <Input
          label="Profile Picture URL"
          {...form.register("profile_picture")}
          placeholder="http://example.com/profile.jpg"
          error={form.formState.errors.profile_picture?.message}
        />
        <Input
          label="Job Title"
          {...form.register("job_title")}
          placeholder="Product Manager"
          error={form.formState.errors.job_title?.message}
        />
        {/* Department Dropdown */}
        <Select
          label="Department"
          name="department"
          options={[
            { value: "Product", label: "Product" },
            { value: "Engineering", label: "Engineering" },
            { value: "Design", label: "Design" },
            { value: "Marketing", label: "Marketing" },
            { value: "Sales", label: "Sales" },
            { value: "HR", label: "HR" },
          ]}
          register={form.register}
          error={form.formState.errors.department?.message}
        />
        <Input
          label="Location"
          {...form.register("location")}
          placeholder="Chicago"
          error={form.formState.errors.location?.message}
        />
        <Textarea
          label="Short Bio"
          {...form.register("short_bio")}
          placeholder="Brief bio..."
          error={form.formState.errors.short_bio?.message}
        />
        <Button type="submit" disabled={isLoading || !form.formState.isValid}>
          {isLoading ? "Adding..." : "Add User"}
        </Button>
      </form>
    </div>
  );
}
