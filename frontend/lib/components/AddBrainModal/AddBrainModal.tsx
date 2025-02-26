import { FormProvider, useForm } from "react-hook-form";

import { addBrainDefaultValues } from "@/lib/config/defaultBrainConfig";

import { AddBrainSteps } from "./components/AddBrainSteps/AddBrainSteps";
import { CreateBrainProps } from "./types";

export const AddBrainModal = (): JSX.Element => {
  const defaultValues: CreateBrainProps = {
    ...addBrainDefaultValues,
    setDefault: true,
    brainCreationStep: "BRAIN_TYPE",
  };

  const methods = useForm<CreateBrainProps>({
    defaultValues,
  });

  return (
    <FormProvider {...methods}>
      <AddBrainSteps />
    </FormProvider>
  );
};
