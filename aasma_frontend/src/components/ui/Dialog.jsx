import * as RadixDialog from '@radix-ui/react-dialog';
import './Dialog.css'; // Ensure you have a corresponding CSS file for styling

export function Dialog({ open, onOpenChange, children }) {
  return (
    <RadixDialog.Root open={open} onOpenChange={onOpenChange}>
      <RadixDialog.Overlay className="dialog-overlay" />
      <RadixDialog.Content className="dialog-content">
        {children}
      </RadixDialog.Content>
    </RadixDialog.Root>
  );
}

export function DialogContent({ children }) {
  return <div className="dialog-content-inner">{children}</div>;
}

export function DialogHeader({ children }) {
  return <div className="dialog-header">{children}</div>;
}

export function DialogTitle({ children }) {
  return <h2 className="dialog-title">{children}</h2>;
}

export function DialogDescription({ children }) {
  return <p className="dialog-description">{children}</p>;
}
